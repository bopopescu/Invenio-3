/** Class providing an interface. The interface markup is create inside HTML,
  * which serves
  *  as a kind of templating system.
  */
function FigureControlsArea(eventsBus, pdfDocument, imageArea){
    /// data slots
    this.eventsBus = eventsBus;
    // current figure
    this.currentFigure = null;
    // interface element displaying current plot and allowing selections
    this.imageArea = imageArea;
    this.pdfDocument = pdfDocument


    /// generating an unique ID that will allow us to identify events
    // registered by this manager
    this.id = "FigureControlsArea" + getNextIdentifier();

    this.rootUIElement = $("#figureControlsLayer");
    /// Claim your interface
    this.lblFigureBoundary = $("#lblFigureBoundary");
    this.lblCaptionBoundary = $("#lblCaptionBoundary");
    this.txtCaptionText = $("#figureCaptionText")

    this.figurePreviewPlaceholder = $("#figurePreviewPalceholder");
    this.figurePreview = new ImageView(this.eventsBus, null,
        this.figurePreviewPlaceholder);

    this.captionPreviewPlaceholder = $("#captionPreviewPlaceholder");
    this.captionPreview = new ImageView(this.eventsBus, null,
        this.captionPreviewPlaceholder);

    this.btnSelectFigureContent = $("#btnSelectFigureContent");
    this.btnSelectCaption = $("#btnSelectFigureCaption");
    this.btnRemoveFigure = $("#btnRemoveFigure");
    
    // reference to save button
    this.btnSave = $("#btnSave");
    // bind to click handler
    this.btnSave.bind(
        "click",
        prepareBoundHandler(this.onBtnSaveClicked, this));
    // reference to save button
    this.btnSave = $("#btnApprove");
    // bind to click handler
    this.btnSave.bind(
        "click",
        prepareBoundHandler(this.onBtnApproveClicked, this));
        
    // reference to save button
    this.btnExtractCaption = $("#btnExtractCaption");
    // bind to click handler
    this.btnExtractCaption.bind(
        "click",
        prepareBoundHandler(this.onBtnExtractCaptionClicked, this));
        
    this.txtCaptionText.bind(
        "change",
        prepareBoundHandler(this.onTxtCaptionTextChanged, this));
        
    // attaching events
    this.btnSelectFigureContent.bind(
        "click",
        prepareBoundHandler(this.onBtnSelectFigureContentClicked, this));

    this.btnSelectCaption.bind(
        "click",
        prepareBoundHandler(this.onBtnSelectCaptiontClicked, this));
    this.btnRemoveFigure.bind(
        "click",
        prepareBoundHandler(this.onBtnRemoveFigureClicked, this));
    
    // reacting to a figure change
    this.eventsBus.registerHandler(Presenter.setFigure, this.id,
        function(subjectId, figure){
            this.setFigure(figure);
        }, this);
    this.noFigureImage = new Image("data/noplot.png", 250, 183);
         
}


FigureControlsArea.onFigureBoundarySelected = "FigureControlsArea.onFigureBoundarySelected";
FigureControlsArea.onFigureCaptionSelected = "FigureControlsArea.onFigureCaptionSelected";

FigureControlsArea.beforeFigureCaptionSelection = "FigureControlsArea.beforeFigureCaptionSelection";

FigureControlsArea.onRemoveFigureClicked = "FigureControlsArea.onRemoveFigureClicked";
FigureControlsArea.onSaveClicked = "FigureControlsArea.onSaveClicked";
FigureControlsArea.onApproveClicked = "FigureControlsArea.onApproveClicked";
FigureControlsArea.onExtractCaptionClicked = "FigureControlsArea.onBtnExtractCaptionClicked";
FigureControlsArea.onTxtCaptionTextChanged = "FigureControlsArea.onTxtCaptionTextChanged";

FigureControlsArea.prototype.getRootUIElement = function(){
    return this.rootUIElement;
};

FigureControlsArea.prototype.enableInterface = function(){
    this.btnSelectFigureContent.removeAttr("disabled");
    this.btnSelectCaption.removeAttr("disabled");
    this.btnRemoveFigure.removeAttr("disabled");
};

FigureControlsArea.prototype.disableInterface = function(){
    this.btnSelectFigureContent.attr("disabled", "true");
    this.btnSelectCaption.attr("disabled", "true");
    this.btnRemoveFigure.attr("disabled", "true");
};

FigureControlsArea.prototype.setFigure = function(newFigure){
    if (this.currentFigure != null && this.currentFigure != undefined){
        this.eventsBus.unregisterHandler(Presenter.figureChanged,
            this.id, this.currentFigure.id);
    }

    this.currentFigure = newFigure;
    if (this.currentFigure != null && this.currentFigure != undefined){
        this.figurePreview.setImage(this.currentFigure.getFigureBoundary().page.image);
        this.captionPreview.setImage(this.currentFigure.getCaptionBoundary().page.image);
        this.eventsBus.registerHandler(Presenter.figureChanged,
            this.id, this.onFigureDataChanged,
            this, this.currentFigure.id);
    }

    // now registering event handlers corresponding to this interface

    this.refreshInterface();
};

/** Redrawing the interface for controling details of a plot
  */
FigureControlsArea.prototype.refreshInterface = function(){
    var image = null
    var captionImage = null;
    var captionText = null;
    var boundaryString = "";
    var captionBoundaryString = "";
    var boundary = null;
    var boundaryCaption = null;
    var figureAngle =0;
    var captionAngle =0;

    if (this.currentFigure == null){
        this.disableInterface();
        image = this.noFigureImage;
        captionImage = null;
        boundary = new Rectangle(0, 0, 250, 183);
        boundaryCaption = new Rectangle(0, 0, 0, 0);
    } else {
        this.enableInterface();
        image = this.currentFigure.getFigureBoundary().page.image;
        captionImage = this.currentFigure.getCaptionBoundary().page.image;
        
        boundaryString = this.currentFigure.getFigureBoundary().rectangle.toString();
        captionBoundaryString = this.currentFigure.getCaptionBoundary().rectangle.toString();
        
        boundary = this.currentFigure.getFigureBoundary().rectangle;
        boundaryCaption = this.currentFigure.getCaptionBoundary().rectangle;
        
        figureAngle = this.currentFigure.getFigureBoundary().rectangle.angle;
        captionAngle = this.currentFigure.getCaptionBoundary().rectangle.angle;
    }


    this.figurePreview.setImage(image);
    this.figurePreview.draw(
        boundary,
        new Rectangle(0, 0, 300, 300), figureAngle, true, true);

    this.captionPreview.setImage(captionImage);
    this.captionPreview.draw(
        boundaryCaption,
        new Rectangle(0, 0, 300, 300), captionAngle, true, false);
    
    if(this.currentFigure != null){
        this.lblFigureBoundary.html(boundaryString);
        this.lblCaptionBoundary.html(captionBoundaryString);
        this.txtCaptionText.val(this.currentFigure.getCaption());
    }
};

FigureControlsArea.prototype.contentSelectionEnded = function(selection){
    this.eventsBus.raise(FigureControlsArea.onFigureBoundarySelected, this.id, [selection])
    this.enableInterface();
};

FigureControlsArea.prototype.onBtnSelectFigureContentClicked = function(){
    this.disableInterface();
    this.imageArea.selectRectangle(prepareBoundHandler(this.contentSelectionEnded, this));
};

FigureControlsArea.prototype.onBtnRemoveFigureClicked = function(){
    this.eventsBus.raise(FigureControlsArea.onRemoveFigureClicked,
        this.id, [this.currentFigure]);
};

FigureControlsArea.prototype.onBtnExtractCaptionClicked = function(){
    this.eventsBus.raise(FigureControlsArea.onExtractCaptionClicked,
        this.id, [this.currentFigure]);
};

FigureControlsArea.prototype.onBtnApproveClicked = function(){
    this.eventsBus.raise(FigureControlsArea.onApproveClicked,
        this.id, []);
};

/***
 * saves the caption to the current figure if it has been changed. 
 * 
 */ 
FigureControlsArea.prototype.onTxtCaptionTextChanged = function(){
    if(this.currentFigure != null && this.currentFigure != undefined){
        this.currentFigure.setCaption(this.txtCaptionText.val());
        this.refreshInterface();
    }
    
/*
    this.eventsBus.raise(FigureControlsArea.onTxtCaptionTextChanged,
        this.id, [this.currentFigure]);
    */
};

FigureControlsArea.prototype.onBtnSaveClicked = function(){
    this.eventsBus.raise(FigureControlsArea.onSaveClicked,
        this.id, []);
};

FigureControlsArea.prototype.captionSelectionEnded = function(selection){
    this.eventsBus.raise(FigureControlsArea.onFigureCaptionSelected, this.id, [selection]);
    this.enableInterface();
};


/**the button for starting the selection of the caption clicked
  */
FigureControlsArea.prototype.onBtnSelectCaptiontClicked = function(){
    this.disableInterface();
    this.eventsBus.raise(FigureControlsArea.beforeFigureCaptionSelection, this.id, []);
    this.imageArea.selectRectangle(prepareBoundHandler(this.captionSelectionEnded, this));
}


/** a handler called when the data of a current figure changed
  */
FigureControlsArea.prototype.onFigureDataChanged = function(subjectId, figure){
    this.refreshInterface();
};
