function query(queryString, onResponse) {
    const xhr = new XMLHttpRequest();
    xhr.responseType = 'json';
    xhr.open("POST", '/graphiql/');
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Accept", "application/json");
    xhr.onload = () => onResponse(xhr.response.data);
    xhr.send(JSON.stringify({query: queryString}));
}


class App extends React.Component {
    constructor(props) {
        super(props);

        this.fetchData = this.fetchData.bind(this);
        this.addToCart = this.addToCart.bind(this);
        this.getProduct = this.getProduct.bind(this);
        this.showingProducts = this.showingProducts.bind(this);

        this.state = {
            stalls: null,
            products: null, // General list of all products
            cart: App.setUpCart(),
            search: null,
            activeStall: null,
            showingProducts: null
        };

        this.fetchData();
    }

    static setUpCart() {
        if (localStorage.cart === undefined) {
            localStorage.cart = JSON.stringify([]);
            return [];
        }

        let cart = [];

        function resetCart() {
            localStorage.cart = JSON.stringify([]);
        }

        try {
            cart = JSON.parse(localStorage.cart);
        } catch (e) {
            resetCart();
            return [];
        }

        if (!Array.isArray(cart)) {
            resetCart();
            return [];
        }

        return cart;
    }

    fetchData() {
        query(`
        {
          stalls {
            id
            name
            activeProducts {
              id
              name
              description
              image
              isSingular
              recommendations
              producttierSet {
                id
                name
                currentPrice
                quantity
              }
            }
          }
        }
        `, result => {

            function processProducts(stall) {
                stall.activeProducts.forEach(product => {
                    // Add stall name to products
                    product.stall = stall.name;

                    // Transform product links to image objects
                    const link = product.image;

                    product.image = new Image();
                    product.image.src = link;
                });

                return stall;
            }

            const stalls = result.stalls.map(stall => {
                return processProducts(stall)
            });

            // Collects all products
            let products = stalls.map(stall => {
                return stall.activeProducts
            }).reduce((a, b) => {
                return a.concat(b);
            });

            this.state.products = products;

            // Map ID to a product image, name an ID
            products = products.map(product => {
                if (product.recommendations.length >= 1) {
                    product.recommendations = product.recommendations.map(id => {
                        const recommendedProduct = this.getProduct(id);
                        return {
                            image: recommendedProduct.image,
                            name: recommendedProduct.name,
                            id: recommendedProduct.id
                        }
                    });
                }

                return product
            });

            this.setState({
                stalls: stalls,
                products: products
            });

        });


    }

    addToCart(tierID, quantity) {
        let cart = this.state.cart;
        let tierInCart = false;

        cart.forEach(item => {
            if (item.tier === tierID) {
                tierInCart = true;
                item.quantity += quantity;
            }
        });

        if (!tierInCart) {
            cart.push({
                tier: tierID,
                quantity: quantity
            });
        }

        localStorage.cart = JSON.stringify(cart);
        this.setState({
            cart: cart
        })
    }

    getProduct(id) {
        const products = this.state.products;
        id = id.toString(); // Must be string

        return products.filter(product => product.id === id)[0];
    }

    showingProducts() {
        if (this.state.stalls === null) {
            //TODO: Show loading state
            return null;
        }

        let products = this.state.products;

        if (this.state.activeStall) {
            products = this.state.activeStall.activeProducts;
        }

        if (this.state.search) {
            // Lower casing allows case insensitivity
            const searchQuery = this.state.search.toLowerCase();

            products = products.filter(product => {
                const productName = product.name.toLowerCase();
                const productDescription = product.description.toLowerCase();
                const stall = product.stall.toLowerCase();

                return productName.includes(searchQuery) || productDescription.includes(searchQuery) || stall.includes(searchQuery);
            })
        }


        return products;
    }

    render() {
        const setActiveStall = stall => {
            this.setState({
                activeStall: stall
            })
        };

        const resetState = () => {
            this.setState({
                activeStall: null,
            });
        };

        const search = query => {
            this.setState({
                search: query
            })
        };

        return (
            <div class="container-fluid p-0 m-0 h-100">
                <Navbar resetState={resetState}
                        search={search}
                        cartCount={this.state.cart.length}/>
                <ProductsBrowser stalls={this.state.stalls}
                                 activeStall={this.state.activeStall}
                                 setActiveStall={setActiveStall}
                                 showingProducts={this.showingProducts()}
                                 searchQuery={this.state.search}
                                 addToCart={this.addToCart}
                                 getProduct={this.getProduct}/>
            </div>
        );
    }
}

ReactDOM.render(
    <App/>,
    document.getElementById('app-container')
);
