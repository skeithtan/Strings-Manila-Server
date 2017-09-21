class ProductsBrowser extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div className="container site-margin mt-3">
                <div className="row">
                    <Collections collections={this.props.collections}
                            activeCollection={this.props.activeCollection}
                            setActiveCollection={this.props.setActiveCollection}/>
                    <Products products={this.props.showingProducts}
                              activeCollection={this.props.activeCollection}
                              searchQuery={this.props.searchQuery}
                              addToCart={this.props.addToCart}
                              getProduct={this.props.getProduct}/>
                </div>
            </div>
        )
    }
}

class Collections extends React.Component {
    constructor(props) {
        super(props);

        this.collectionItems = this.collectionItems.bind(this);
    }

    collectionItems() {
        if (this.props.collections === null) {
            return null;
        }

        const activeCollection = this.props.activeCollection;

        const collections = this.props.collections.map(collection => {
            const isActive = activeCollection === null ? false : collection.id === activeCollection.id;

            return <CollectionItem key={collection.id}
                              collection={collection}
                              isActive={isActive}
                              setActiveCollection={this.props.setActiveCollection}/>
        });

        return (
            <li className="list-group">
                {collections}
            </li>
        )
    }

    render() {
        return (
            <div className="col-lg-3">
                <h2 className="mb-3 mt-3">Collections</h2>
                {this.collectionItems()}
            </div>
        )
    }
}

class CollectionItem extends React.Component {
    constructor(props) {
        super(props);
        this.activeItem = this.activeItem.bind(this);
        this.inactiveItem = this.inactiveItem.bind(this);
    }

    activeItem() {
        return (
            <li className="list-group-item bg-dark text-light">{this.props.collection.name}</li>
        )
    }

    inactiveItem() {
        return (
            <li className="list-group-item"
                onClick={() => {
                    this.props.setActiveCollection(this.props.collection);
                }}>{this.props.collection.name}</li>
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
            if (this.props.activeCollection) {
                return (
                    <h2 className="mt-5 text-center">Searching for
                        <span className="text-muted"> {this.props.searchQuery} </span>
                        in
                        <span className="text-muted"> {this.props.activeCollection.name} </span>
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

        if (this.props.activeCollection === null) {
            return null;
        }

        return (
            <h2 className="mt-5 text-center">{this.props.activeCollection.name}</h2>
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
                                addToCart={this.props.addToCart}
                                getProduct={this.props.getProduct}/>
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
        this.image = this.image.bind(this);
    }

    image() {
        const image = this.props.product.image;
        return <img src={image.src} className="card-img-top bg-light"/>;
    }

    render() {
        return (
            <div className="card bg-white mb-3 border-0"
                 data-toggle="modal"
                 data-target="#product-card-modal"
                 onClick={() => onProductCardClick(this.props.product, this.props.addToCart, this.props.getProduct)}>
                {this.image()}
                <div className="card-body">
                    <h4 className="card-title">{this.props.product.name}</h4>
                    <p className="card-text text-muted">{this.props.product.description}</p>
                </div>
                <div className="card-footer">
                    <h5 className="mb-0">₱{this.props.product.producttierSet[0].currentPrice}</h5>
                </div>
            </div>
        )
    }
}

