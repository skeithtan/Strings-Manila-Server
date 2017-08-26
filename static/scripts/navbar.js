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
                        <input className="form-control w-100 mr-auto col-lg-5 bg-dark text-white border-secondary"
                               placeholder="Search products"
                               onChange={this.search}/>
                        <ul className="navbar-nav ml-auto">
                            <li className="nav-item">
                                <button className="btn btn-outline-secondary border-light text-light ml-5">
                                    Cart {this.badge()}</button>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        )
    }
}