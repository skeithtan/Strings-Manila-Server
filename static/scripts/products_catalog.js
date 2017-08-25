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

    showingProducts() {
        if (this.state.stalls === null) {
            //TODO: Show loading state
            return null;
        }

        if (this.state.activeStall === null) {
            //Collect all products
            return this.state.stalls
                .map(stall => {
                    return stall.activeProducts
                })
                .reduce((a, b) => {
                    return a.concat(b);
                })
        }

        return this.state.activeStall.activeProducts;
    }

    render() {
        const setActiveStall = stall => {
            this.setState({
                activeStall: stall
            })
        };

        const removeActiveStall = () => {
            this.setState({
                activeStall: null
            })
        };

        return (
            <div class="container-fluid p-0 m-0 h-100">
                <Navbar removeActiveStall={removeActiveStall}/>
                <ProductsBrowser stalls={this.state.stalls}
                                 activeStall={this.state.activeStall}
                                 setActiveStall={setActiveStall}
                                 showingProducts={this.showingProducts()}/>
            </div>
        );
    }
}

ReactDOM.render(
    <App/>
    ,
    document.getElementById('app-container')
);
