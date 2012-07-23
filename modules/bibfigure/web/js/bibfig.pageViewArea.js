/** A control displaying a page, marking all figures present in a page with rectangles
  * and allowing to resize those rectangles. It allows also to select figures by clicking
  * on their caption or main boundary.
  *
  * The scale of the displayed page can be regulated using scrollers.
  */

function PageViewArea(container, eventsBus){
    this.id = "PageViewArea" + getNextIdentifier();
    // building the interface
    this.rootElement = container;
    this.mainElement = $("<div class=\"ui-pageviewarea-mainelement\"></div>"); // widgets should not put any absolute fixed elements into the container
    this.rootElement.append(this.mainElement);

    this.scrollableContainer = $("<div class=\"pageViewScrollableContainer\"></div>");

    this.imgElement = $("<img></img>");
    this.rectanglesContainer = $("<div class=\"pageViewRectanglesContainer\"></div>");
    this.controlsArea = $("<div class=\"pageViewZoomControls\"></div>")

    this.mainElement.append(this.scrollableContainer);

    this.scrollableContainer.append(this.imgElement);
    this.scrollableContainer.append(this.rectanglesContainer);

    this.mainElement.append(this.controlsArea);

    // building the zoom area


    this.zoomSlider = $("<div class=\"pageViewZoomSlider\"></div>");
    this.lblZoomScale = $("<p>100%</p>");

    this.controlsArea.append(this.lblZoomScale);
    this.controlsArea.append(this.zoomSlider);

    this.zoomSlider.slider({
        orientation: "vertical",
        range: "min",
        min: 30,
        max: 300,
        value: 100,
        slide: prepareBoundHandler(function(event, ui){
            this.zoomToScale(ui.value / 100);
        }, this)
    });

    // the rotation slider
    this.rotationSlider = $("<div class=\"pageViewRotationSlider\"></div>");
    this.lblRotationAngle = $("<div style=\"position: relative; height:50px; display: block;\">0 &deg;</div>");
    
    this.rotationSlider.slider({
        orientation: "vertical",
        min: -180,
        max: 180,
        value: 0,
        slide: prepareBoundHandler(function(event, ui){
            var angle = ui.value;
            this.rotateToAngle(angle);
        }, this)
    });
    this.btnResetRotation = $("<input type=\"button\" id=\"btnResetRotation\" value=\"0&deg;\" />");
    this.btnResetRotation.bind(
        "click",
        prepareBoundHandler(function(){
            this.rotateToAngle(0);
        }, this));
        
    this.btnResetZoom = $("<input type=\"button\" id=\"btnResetZoom\" value=\"100%\" />");
    this.btnResetZoom.bind(
        "click",
        prepareBoundHandler(function(){
            this.zoomSlider.slider("value", 100);
            this.zoomSlider.slider("refresh");
            this.zoomToScale(1);
        }, this));
    this.controlsArea.append(this.btnResetZoom)
    this.controlsArea.append(this.lblRotationAngle);
    
    this.controlsArea.append(this.rotationSlider);
    
    this.controlsArea.append(this.btnResetRotation);

    // claiming additional data
    this.eventsBus = eventsBus;

    // update the page image when page has been changed
    this.eventsBus.registerHandler(Presenter.setPage, this.id,
        function(subjectId, page){
            pdfDocument = page.pdfDocument;
            
            this.page = page;
            this.setPageImage(page.image);
            this.adjustImage();
            // drawing all the figures form the page
            this.clearMarkup();
            
            for (var fId in pdfDocument.getFigures()){
                
                if(pdfDocument.figures[fId].getCaptionBoundary().page == this.page){
                    this.addCaptionRectangle(pdfDocument.figures[fId]);
                }
                if(pdfDocument.figures[fId].getFigureBoundary().page == this.page){
                    this.addFigureRectangle(pdfDocument.figures[fId]);
                }
                
            }
            
        }, this);

    // we need to handle the creation of new figures - we want to highlight them
    // imemdiately

    this.eventsBus.registerHandler(Presenter.figureCreated, this.id,
        function(subjectId, figure){
            if(figure.getCaptionBoundary().page == this.page){
                this.addCaptionRectangle(figure);
            }
            if(figure.getFigureBoundary().page == this.page){
                this.addFigureRectangle(figure);
            }
        }, this);

    this.eventsBus.registerHandler(
        Presenter.figureChanged, this.id,
        function(subjectId, figure){
            if (this.page == figure.getFigureBoundary().page){
                if (this.figToRectangles[figure.id] != undefined){
                    this.figToRectangles[figure.id].setRectangle(figure.getFigureBoundary().rectangle);
                } else { // figure has been modified and now is present on our page
                    this.addFigureRectangle(figure);
                }
                
                
            } else {
                if (this.figToRectangles[figure.id] != undefined){ // figure moved from current page... could not happen with current interface but mabe in the future
                    alert("figure moved out of current page ... please implement the removal of the frame");
                }
            }
            
            
            if (this.page == figure.getCaptionBoundary().page){
                if (this.captToRectangles[figure.id] != undefined){
                    this.captToRectangles[figure.id].setRectangle(figure.getCaptionBoundary().rectangle);
                } else { // figure has been modified and now is present on our page
                    this.addCaptionRectangle(figure);
                }
                
                
            } else {
                if (this.captToRectangles[figure.id] != undefined){ // figure moved from current page... could not happen with current interface but mabe in the future
                    alert("figure moved out of current page ... please implement the removal of the frame");
                }
            }
            
            
        }, this);

    this.eventsBus.registerHandler(
        Presenter.figureRemoved, this.id,
        function(subjectId, figure){
            if (this.page == figure.page
                && this.figToRectangles[figure.id] != undefined){
                this.figToRectangles[figure.id].getRootUIElement().remove();
                delete this.figToRectangles[figure.id];
            }
        }, this);

    this.rectangles = [];
    this.figToRectangles = {};
    this.captToRectangles = {};
    this.scale = 1;
    this.rotationAngle = 0;

    this.page = null;

}

PageViewArea.prototype.getRootUIElement = function(){
    return this.rootElement;
};

PageViewArea.prototype.rotateToAngle = function(newAngle){
    this.rotationAngle = newAngle;
    this.lblRotationAngle.html(newAngle + "&deg;");
    // TODO: ajust covering rectangles
    this.adjustImage();
}

PageViewArea.prototype.zoomToScale = function(newScale){
    this.lblZoomScale.html(Math.floor(newScale*100) + "%");
    // here calculate the central document point according to current scroll value
    var scrollableView = this.scrollableContainer;

    var scrolledX = scrollableView.scrollLeft();
    var scrolledY = scrollableView.scrollTop();
    var viewWidth = scrollableView.width();
    var viewHeight = scrollableView.height();
    var documentWidth = (this.page == null) ? 0 : this.page.image.width;
    var documentHeight = (this.page == null) ? 0 : this.page.image.height;

    // following values are floating point !!!
    var centerX = (scrolledX + viewWidth / 2) / this.scale;
    var centerY = (scrolledY + viewHeight / 2) / this.scale;
    
    // change the document scale

    this.setScale(newScale);

    // calculate the scrolling value based on the center of the document
    var newScrollX = (centerX * newScale) - (viewWidth / 2);
    var newScrollY = (centerY * newScale) - (viewHeight / 2);


    if (newScrollX > documentWidth * newScale - viewWidth){
        newScrollX = documentWidth * newScale - viewWidth;
    }
    if (newScrollX > documentHeight * newScale - viewHeight){
        newScrollX = documentHeight * newScale - viewHeight;
    }

    // the below possibly fixes problem caused by above assignment, but also standard zoom
    if (newScrollX < 0){
        newScrollX = 0;
    }

    if (newScrollY < 0){
        newScrollY = 0;
    }
    scrollableView.scrollLeft(newScrollX);
    scrollableView.scrollTop(newScrollY);
};

PageViewArea.prototype.addCaptionRectangle = function(figure){
    // add caption rectangle
    var captRectangle = this.addRectangle(figure.getCaptionBoundary().rectangle, "imageSelectedRectangleCaption");
    this.captToRectangles[figure.id] = captRectangle;
};

PageViewArea.prototype.addFigureRectangle = function(figure){
    var rectangle = this.addRectangle(figure.getFigureBoundary().rectangle.copy());
    this.figToRectangles[figure.id] = rectangle;
};

PageViewArea.prototype.setScale = function(newScale){
    this.scale = newScale;
    this.adjustImage();
}




/** Adjusting image parameters to the situation described by scale and angle*/

PageViewArea.prototype.adjustImage = function(){
    

    
    
    // TODO: make it work
    
    var newScale = 1. 
    if(this.scale > 2.){
        this.setPageImage(this.page.image, true)
        newScale = 2.;
    }
    else{
        this.setPageImage(this.page.image, false)
    }
    
    var css = getTransformedCSS(this.rotationAngle, this.scale/newScale,
        this.page.image.width,
        this.page.image.height);
    // visualising the changes
    this.imgElement.css(css);
    

    // updating rectangles drawn on the page
    for (var recId in this.rectangles){
        this.rectangles[recId].setPageRectangle(new Rectangle(0, 0, this.page.image.width, this.page.image.height));
        this.rectangles[recId].setAngle(this.rotationAngle);
        this.rectangles[recId].setScale(this.scale);
    }

};

PageViewArea.prototype.selectRectangle = function(onFinish){
    var me = this;
    this.hideAdditionalInterface();
    $("body").css({
        cursor: "crosshair"
    });
    this.imgElement.imgAreaSelect({
        handles: false,
        onSelectEnd: function(img, selection){
            me.imgElement.imgAreaSelect({
                remove:true
            });
            me.showAdditionalInterface();

            // rescaling the selection current scale -> 1.0
            var x = Math.round(selection.x1 / me.scale);
            var y = Math.round(selection.y1 / me.scale);

            var width = Math.round(selection.width / me.scale);
            var height = Math.round(selection.height / me.scale);

            $("body").css({
                cursor: "auto"
            });
            onFinish(new Rectangle(x, y, width, height, me.rotationAngle));
        },
        persistent: false
    });
};


PageViewArea.prototype.clearMarkup = function(){
    this.rectanglesContainer.empty();
    this.rectangles = [];
    this.figToRectangles = {};
    this.captToRectangles = {};
};

/**
 * Add a rectangle marking a plot to the interface
 */
PageViewArea.prototype.addRectangle = function(rectangle, cssStyle){
    cssStyle = cssStyle || "imageSelectedRectangle";
    var pRec = new Rectangle(0,0, this.page.image.width, this.page.image.height);
    var rectangleC = new PageViewRectangle(rectangle, cssStyle, this.scale,
        pRec, this.rotationAngle);
        

    this.rectanglesContainer.append(rectangleC.getRootUIElement());
    this.rectangles.push(rectangleC);
    return rectangleC;
};

PageViewArea.prototype.setPageImage = function(image, highdef){
    
    highdef = typeof highdef !== 'undefined' ? highdef : false;
    if (image != null && image != undefined){
        if(highdef){
            this.imgElement.attr("src", image.getUrlHD());
        }
        else{
            this.imgElement.attr("src", image.getUrl());
        }
        
    //this.adjustImage();
    }
};

PageViewArea.prototype.hideAdditionalInterface = function(){
    this.controlsArea.css({
        display: "none"
    });
    this.rectanglesContainer.css({
        display: "none"
    });
};


PageViewArea.prototype.showAdditionalInterface = function(){
    this.controlsArea.css({
        display: "block"
    });
    this.rectanglesContainer.css({
        display: "block"
    });
};




/** an interface element displaying a rectangle in the page view interface */

function PageViewRectangle(rectangle, cssStyle, scale, pageRectangle, angle){
    this.id = "PageViewRectangle" + getNextIdentifier();

    this.scale =  (scale == undefined || scale == null) ? 1 : scale;
    this.viewAngle =  (angle == undefined || angle == null) ? 0 : angle;
    this.pageRectangle =  (pageRectangle == undefined || pageRectangle == null) ? new Rectangle(0, 0, 0, 0) : pageRectangle;

    this.rectangle = rectangle;
    this.rootUIElement = $("<div class=\"" + cssStyle + "\"></div>");

    this.setPageRectangle(this.pageRectangle);
    this.setAngle(this.viewAngle);
    this.setScale(this.scale);
}

PageViewRectangle.getPageVertices = function(){
    var points = new Array()
    
    points[0] = {
        "x": this.rectangle.x, 
        "y": this.rectangle.y
    };
    points[1] = {
        "x": this.rectangle.x + this.rectangle.width, 
        "y": this.rectangle.y
    };
    points[2] = {
        "x": this.rectangle.x + this.rectangle.width, 
        "y": this.rectangle.y + this.rectangle.height
    };
    points[3] = {
        "x": this.rectangle.x, 
        "y": this.rectangle.y + this.rectangle.height
    };
    
    
    var p = {
        "x": 100, 
        "y": 100
    };
    var effX = Math.round(this.rectangle.x * 1.);
    var effY = Math.round(this.rectangle.y * 1.);
    var effWidth = Math.round(this.rectangle.width * 1.);
    var effHeight = Math.round(this.rectangle.height * 1.);

    var tm1 = getTransformedMargin(this.rectangle.angle,
        1,
        this.pageRectangle.width,
        this.pageRectangle.height);

    // set view angle to zero
    var tm2 = getTransformedMargin(0.,
        1,
        this.pageRectangle.width,
        this.pageRectangle.height);
 
    var originCss = "" + (-effX) + "px " + (-effY)+"px";
    
    
    var bringToOrthoCss = "translate(" + (-tm1.x) + "px, " + (-tm1.y) + "px)";

    var rotateCss = "rotate(" + (this.viewAngle - this.rectangle.angle) + "deg)";

    var returnFromOrthoCss = "translate(" + tm2.x + "px, " + tm2.y + "px)";

    var transCss = returnFromOrthoCss + " " + rotateCss + " " + bringToOrthoCss;
    debugger;
    // translate to origin of rotation
    //p = translation(p, effX, effY);
    
    // return from ortho
    p = translation(p, tm2.x, tm2.y);
    // rotate
    p = rotation(p,  - this.rectangle.angle);
    // bring to ortho
    p = translatation(p, -tm1.x, -tm1.y);
    
    // bring back from origin
    //p = translation(p, -effX, -effY);
}

PageViewRectangle.prototype.refresh = function(){
    var effX = Math.round(this.rectangle.x * this.scale);
    var effY = Math.round(this.rectangle.y * this.scale);
    var effWidth = Math.round(this.rectangle.width * this.scale);
    var effHeight = Math.round(this.rectangle.height * this.scale);

    var tm1 = getTransformedMargin(this.rectangle.angle,
        this.scale,
        this.pageRectangle.width,
        this.pageRectangle.height);

    var tm2 = getTransformedMargin(this.viewAngle,
        this.scale,
        this.pageRectangle.width,
        this.pageRectangle.height);

    var originCss = "" + (-effX) + "px " + (-effY)+"px";
    var bringToOrthoCss = "translate(" + (-tm1.x) + "px, " + (-tm1.y) + "px)";

    var rotateCss = "rotate(" + (this.viewAngle - this.rectangle.angle) + "deg)";

    var returnFromOrthoCss = "translate(" + tm2.x + "px, " + tm2.y + "px)";

    var transCss = returnFromOrthoCss + " " + rotateCss + " " + bringToOrthoCss;

    cssmap = {
        "position": "absolute",
        "width": effWidth + "px",
        "height": effHeight + "px",
        "left": effX + "px",
        "top": effY + "px",
        "-moz-transform-origin" : originCss,
        "-moz-transform" : transCss,
        "-webkit-transform-origin" : originCss,
        "-webkit-transform" : transCss
    }
    this.rootUIElement.css(cssmap)
}

PageViewRectangle.prototype.setScale = function(scale){
    this.scale = scale;
    this.refresh();
};

PageViewRectangle.prototype.setAngle = function(angle){
    this.viewAngle = angle;
    this.refresh();
};

PageViewRectangle.prototype.getRootUIElement = function(){
    return this.rootUIElement;
};

PageViewRectangle.prototype.setRectangle = function(newRectangle){
    this.rectangle = newRectangle;
    this.refresh();
};

/** Set a not scaled page rectangle
  */

PageViewRectangle.prototype.setPageRectangle = function(pageRectangle){
    this.pageRectangle = pageRectangle;
    this.refresh();
};


