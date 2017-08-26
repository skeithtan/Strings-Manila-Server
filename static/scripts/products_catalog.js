class App extends React.Component {
    constructor(props) {
        super(props);

        this.fetchData = this.fetchData.bind(this);
        this.addToCart = this.addToCart.bind(this);
        this.showingProducts = this.showingProducts.bind(this);

        this.state = {
            stalls: null,
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
              producttierSet {
                id
                name
                currentPrice
              }
            }
          }
        }
        `, result => {
            this.setState({
                stalls: result.stalls
            })
        });
    }

    addToCart(tierID, quantity) {
        let cart = this.state.cart;
        let tierInCart = false;

        console.log(quantity);

        cart.forEach(item => {
            console.log(item);
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

    showingProducts() {
        if (this.state.stalls === null) {
            //TODO: Show loading state
            return null;
        }

        let products;

        if (this.state.activeStall === null) {
            //Collect all products
            products = this.state.stalls
                .map(stall => {
                    return stall.activeProducts
                })
                .reduce((a, b) => {
                    return a.concat(b);
                });
        } else {
            products = this.state.activeStall.activeProducts;
        }

        if (this.state.search) {
            // Lower casing allows case insensitivity
            const searchQuery = this.state.search.toLowerCase();

            products = products.filter(product => {
                const productName = product.name.toLowerCase();
                const productDescription = product.description.toLowerCase();

                return productName.includes(searchQuery) || productDescription.includes(searchQuery);
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
                                 addToCart={this.addToCart}/>
            </div>
        );
    }
}

ReactDOM.render(
    <App/>,
    document.getElementById('app-container')
);
