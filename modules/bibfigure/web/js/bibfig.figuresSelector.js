/** selector of figures */
function FiguresSelector(container, eventsBus, pdfDocument, entryWidth, entryHeight){
    // claim your data
    this.id = "FiguresSelector" + getNextIdentifier();
    this.parent = container;

    this.eventsBus = eventsBus;
    this.internalEventsBus = new EventsBus();
    // we want to separate internal events and emit only global

    this.pdfDocument = pdfDocument;

    this.entryWidth = entryWidth;
    this.entryHeight = entryHeight;

    // claim your interface
    this.selectorPlaceholder = $("#figureMiniaturesSelector");
    this.selector = new Selector(this.internalEventsBus, this.selectorPlaceholder, "horizontal");

    this.createNewFigureClicked = $("#btnNewPlot");
    // claim your events

    this.createNewFigureClicked.bind(
        "click",
        prepareBoundHandler(this.onNewFigureClickedHandler, this));

    this.eventsBus.registerHandler(Presenter.figureCreated,
        this.id,
        this.onNewFigureCreatedHandler,
        this);

    this.onCreateNewFigure = new EventHandler();
    this.figuresToOptions = {};

    this.eventsBus.registerHandler(Presenter.setFigure, this.id,
        function(subjectId, currentFigure){
            this.setCurrentFigure(currentFigure);
        }, this);

    this.eventsBus.registerHandler(Presenter.figureRemoved, this.id,
        function(subjectId, figure){
            this.removeFigure(figure);
        }, this);
}

FiguresSelector.onFigureSelected = "FiguresSelector.onFigureSelected";

FiguresSelector.prototype.getRootUIElement = function(){
    return this.parent;
};

/** sets the currently selected figure
  */
FiguresSelector.prototype.setCurrentFigure = function(newFigure){
    this.figuresToOptions[newFigure.id].select();
};


FiguresSelector.prototype.removeFigure = function(figure){
    if (this.figuresToOptions[figure.id] == undefined){
        return;
    }

    // removing the interface element
    this.selector.removeOption(this.figuresToOptions[figure.id]);
    delete this.figuresToOptions[figure.id];
};

/** Create new selector for a single plot */
FiguresSelector.prototype.addFigureOption = function(figure){
    var figureOption = new SelectorOption(this.internalEventsBus, this.selector);
    // figure view has to listen to the main event queue ! It reacts to figure changes
    var imageViewer = new FigureView(this.eventsBus, figure,
        new Rectangle(0, 0, 100, 100),
        true, true);

    figureOption.setContent(imageViewer.getRootUIElement());


    this.internalEventsBus.registerHandler(
        SelectorOption.onSelected, this.id,
        function(subjectId, figureId){
            this.eventsBus.raise(FiguresSelector.onFigureSelected, this.id, [figure]);
        }, this,
        figureOption.id);

    this.figuresToOptions[figure.id] = figureOption;

    return figureOption;
};

FiguresSelector.prototype.onNewFigureClickedHandler = function(){
    this.onCreateNewFigure.invoke([]);
};

FiguresSelector.prototype.onNewFigureCreatedHandler = function(subjectId, figure){
    this.addFigureOption(figure);
};

/** a presenter for a figure */
function FigureView(eventsBus, figure, boundary, extendH, extendV){
    this.id = "FigureView" + getNextIdentifier();
    this.eventsBus = eventsBus;
    var image = figure ? figure.getFigureBoundary().page.image : null;

    this.imageView = new ImageView(this.eventsBus, image);
    this.boundary = boundary;
    this.figure = null;
    this.extendV = extendV;
    this.extendH = extendH;
    this.setFigure(figure);
}


FigureView.prototype.getRootUIElement = function(){
    return this.imageView.getRootUIElement();
};

/**react to the event of changed figure */
FigureView.prototype.redrawFigure = function(figureId){
    this.imageView.setImage(this.figure.getFigureBoundary().page.image);
    this.imageView.draw(this.figure.getFigureBoundary().rectangle, this.boundary, this.figure.getFigureBoundary().rectangle.angle, this.extendH, this.extendV);
};

/** change the currently attached figure*/
FigureView.prototype.setFigure = function(figure){
    if (this.figure != null && this.figure != undefined){
        caption = $("#figureCaptionText").val();
        this.figure.setCaption(caption);
        
        this.eventsBus.unregisterHandler(Presenter.figureChanged, this.id,
            this.figure.id);
    }
    

    this.figure = figure;

    if (this.figure != null && this.figure != undefined){
        // subscribe for changes of the newly set figure
        this.eventsBus.registerHandler(Presenter.figureChanged, this.id,
            this.redrawFigure, this, this.figure.id);
        this.redrawFigure();
    }
}

