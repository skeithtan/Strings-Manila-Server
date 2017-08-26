class ProductsBrowser extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div className="container site-margin mt-3">
                <div className="row">
                    <Stalls stalls={this.props.stalls}
                            activeStall={this.props.activeStall}
                            setActiveStall={this.props.setActiveStall}/>
                    <Products products={this.props.showingProducts}
                              activeStall={this.props.activeStall}
                              searchQuery={this.props.searchQuery}
                              addToCart={this.props.addToCart}/>
                </div>
            </div>
        )
    }
}

class Stalls extends React.Component {
    constructor(props) {
        super(props);

        this.stallItems = this.stallItems.bind(this);
    }

    stallItems() {
        if (this.props.stalls === null) {
            return null;
        }

        const activeStall = this.props.activeStall;

        const stalls = this.props.stalls.map(stall => {
            const isActive = activeStall === null ? false : stall.id === activeStall.id;

            return <StallItem key={stall.id}
                              stall={stall}
                              isActive={isActive}
                              setActiveStall={this.props.setActiveStall}/>
        });

        return (
            <li className="list-group">
                {stalls}
            </li>
        )
    }

    render() {
        return (
            <div className="col-lg-3">
                <h2 className="mb-3 mt-3">Stalls</h2>
                {this.stallItems()}
            </div>
        )
    }
}

class StallItem extends React.Component {
    constructor(props) {
        super(props);
        this.activeItem = this.activeItem.bind(this);
        this.inactiveItem = this.inactiveItem.bind(this);
    }

    activeItem() {
        return (
            <li className="list-group-item bg-dark text-light">{this.props.stall.name}</li>
        )
    }

    inactiveItem() {
        return (
            <li className="list-group-item"
                onClick={() => {
                    this.props.setActiveStall(this.props.stall);
                }}>{this.props.stall.name}</li>
        )
    }

    render() {
        return this.props.isActive ? this.activeItem() : this.inactiveItem();
    }
}

class Products extends React.Component {
    constructor(props) {
        super(props);
        this.header = this.header.bind(this);
        this.cards = this.cards.bind(this);
    }

    header() {
        if (this.props.searchQuery) {
            if (this.props.activeStall) {
                return (
                    <h2 className="mt-5 text-center">Searching for
                        <span className="text-muted"> {this.props.searchQuery} </span>
                        in
                        <span className="text-muted"> {this.props.activeStall.name} </span>
                    </h2>
                )
            } else {
                return (
                    <h2 className="mt-5 text-center">Searching for
                        <span className="text-muted"> {this.props.searchQuery} </span>
                    </h2>
                )
            }
        }

        if (this.props.activeStall === null) {
            return null;
        }

        return (
            <h2 className="mt-5 text-center">{this.props.activeStall.name}</h2>
        )
    }

    cards() {
        if (this.props.products === null) {
            //TODO: Return loading state
            return null;
        }

        if (this.props.products.length === 0 && this.props.searchQuery) {
            return (
                <div className="container-fluid d-flex flex-column justify-content-center align-items-center h-100 p-5 mt-5 mb-5">
                    <h3>No products found</h3>
                    <h6 className="text-muted">Change your query and try your search again</h6>
                </div>
            )
        }

        const productCards = this.props.products.map(product => {
            return <ProductCard key={product.id}
                                product={product}
                                addToCart={this.props.addToCart}/>
        });

        return (
            <div className="card-deck p-3 pt-5 pb-5"
                 id="products">
                {productCards}
            </div>
        )
    }

    render() {
        return (
            <div className="col-lg-9">
                {this.header()}
                {this.cards()}
            </div>
        )
    }
}

class ProductCard extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="card bg-dark text-light mb-3"
                 data-toggle="modal"
                 data-target="#product-card-modal"
                 onClick={() => onProductCardClick(this.props.product, this.props.addToCart)}>
                <img className="card-img-top"
                     src={this.props.product.image}
                     alt={this.props.product.name}/>
                <div className="card-body">
                    <h4 className="card-title">{this.props.product.name}</h4>
                    <p className="card-text">{this.props.product.description}</p>
                </div>
                <div className="card-footer">
                    <h5 className="mb-0">₱{this.props.product.producttierSet[0].currentPrice}</h5>
                </div>
            </div>
        )
    }
}

