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
                              activeStall={this.props.activeStall}/>
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
        if (this.props.activeStall === null) {
            return null;
        }

        if (this.props.search) {
            if (this.props.activeStall) {
                return (
                    <h2 className="mt-5 text-center">Searching for
                        <span className="text-muted">{this.props.search}</span>
                        in
                        <span className="text-muted">{this.props.activeStall.name}</span>
                    </h2>
                )
            } else {
                return (
                    <h2 className="mt-5 text-center">Searching for
                        <span className="text-muted">{this.props.search}</span>
                    </h2>
                )
            }
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

        return this.props.products.map(product => {
            return <ProductCard key={product.id}
                                product={product}/>
        });
    }

    render() {
        return (
            <div className="col-lg-9">
                {this.header()}
                <div className="card-deck p-3 pt-5 pb-5"
                     id="products">
                    {this.cards()}
                </div>
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
                 onClick={() => onProductCardClick(this.props.product)}>
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

function onProductCardClick(product) {
    $('#product-modal-product-name').html(product.name);
    $('#product-modal-product-price').html("₱" + product.producttierSet[0].currentPrice); //TODO
    $('#product-modal-product-description').html(product.description);
    $('#product-modal-main-product-img').attr('src', product.image);

    if (product.isSingular) {
        $('#product-modal-tiers').hide();
    } else {
        setUpTieredProduct(product.producttierSet)
    }

}

function setUpTieredProduct(tiers) {
    $('#product-modal-tiers').show();
    let isFirst = true;

    function setActiveTier(tier) {
        $('#product-modal-selected-tier').val(tier.id);
        $('#product-modal-product-price').html("₱" + tier.currentPrice);
    }

    $('#product-modal-tier-choices').html(''); //Clear first

    tiers.forEach(tier => {
        const clone = $('#product-modal-tier-button-clone').clone();
        clone.removeAttr('id');
        clone.append(tier.name);
        clone.click(() => {
            setActiveTier(tier);
        });

        const radioButton = $(clone.find('input')[0]);
        radioButton.val(tier.id);

        if (isFirst) {
            console.log(isFirst);
            isFirst = false;
            clone.addClass('active');
            radioButton.attr('checked', true);
            setActiveTier(tier);
        }

        $('#product-modal-tier-choices').append(clone);
    })
}