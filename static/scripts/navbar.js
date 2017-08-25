class Navbar extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <nav className="navbar navbar-expand-lg navbar-dark bg-dark d-block">
                <div className="container site-margin">
                    <a className="navbar-brand m-0 mr-4 text-uppercase font-weight-bold"
                       onClick={this.props.removeActiveStall}
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
                        <input className="form-control w-100 mr-auto"
                               placeholder="Search products"/>
                        <ul className="navbar-nav ml-auto">
                            <li className="nav-item">
                                <button className="btn btn-secondary ml-5">Cart</button>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        )
    }
}