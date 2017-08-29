class Navbar extends React.Component {
    constructor(props) {
        super(props);
        this.search = this.search.bind(this);
        this.badge = this.badge.bind(this);
    }

    search(event) {
        const query = event.target.value;
        this.props.search(query);
    }

    badge() {
        if (this.props.cartCount === 0) {
            return null;
        }

        return (
            <span className="badge badge-light ml-1">{this.props.cartCount}</span>
        )
    }

    signInButton() {
        if (preloadedData.user.isAuthenticated) {
            return (
                <div className="btn-group ml-2">
                    <button type="button"
                            className="btn btn-secondary dropdown-toggle"
                            data-toggle="dropdown"
                            aria-haspopup="true"
                            aria-expanded="false">
                        Hello, {preloadedData.user.name}
                    </button>
                    <div className="dropdown-menu">
                        <a className="dropdown-item"
                           href="/profile/">Profile</a>
                        <a className="dropdown-item"
                           href="#">Orders</a>
                        <a className="dropdown-item"
                           href="/waitlist/">Waitlists</a>
                        <hr className="dropdown-divider" />
                        <button className="dropdown-item"
                                id="sign-out-button">Sign out
                        </button>
                    </div>
                </div>
            )
        } else {
            return (
                <a href="/accounts/facebook/login/?process=login"
                   className="btn btn-primary ml-2">Sign in with
                    Facebook</a>
            )
        }
    }

    render() {
        return (
            <nav className="navbar navbar-expand-lg navbar-dark bg-dark d-block">
                <div className="container site-margin">
                    <a className="navbar-brand m-0 mr-4 text-uppercase font-weight-bold"
                       onClick={this.props.resetState}
                       href="#">Strings Manila</a>
                    <button className="navbar-toggler"
                            type="button"
                            data-toggle="collapse"
                            data-target="#navbarNavDropdown"
                            aria-controls="navbarNavDropdown"
                            aria-expanded="false"
                            aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>

                    <div className="collapse navbar-collapse"
                         id="navbarNavDropdown">
                        <input className="form-control w-100 mr-auto bg-dark text-white border-secondary"
                               type="search"
                               placeholder="Search products"
                               onChange={this.search}
                               id="search-bar"/>
                        <ul className="navbar-nav ml-auto">
                            <li className="nav-item mr-2">
                                <a href="/cart/" className="btn btn-outline-secondary border-light text-light ml-5">
                                    Cart {this.badge()}</a>
                            </li>
                            <li className="nav-item d-flex align-items-center justify-content-center">
                                {this.signInButton()}
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        )
    }
}