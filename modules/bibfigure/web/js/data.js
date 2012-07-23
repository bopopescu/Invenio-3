/** The model of the data used by the plots selector
 */


/** a class representing the image */
function Image(url, width, height){
    this.url = url;
    this.width = width;
    this.height = height;
}

/**
   angle -> angle under which the rectangle is paralel to the x,y axis with x,y equal to given parameters
*/

function Rectangle(x, y, width, height, angle){
    this.x = x || 0;
    this.y = y || 0;
    this.width = width || 0;
    this.height = height || 0;
    this.angle = angle || 0;
}

Rectangle.prototype.toString = function(){
    return "(x = " + this.x + ", y = " + this.y + ", width = "
	+ this.width + ", height = " + this.height + ")";
};

/** Get a scale allowing to fit the rectangle into a given box.
  * The scale is equal to the ratio: new width/ new height
  */
Rectangle.prototype.getFittingScale = function(view){
    var ratio = this.width / this.height;
    var limitRatio = view.width / view.height;
    return ratio > limitRatio ?
	view.width / this.width
	: view.height / this.height;
};

function Figure(page){
    this.id = "Figure" + getNextIdentifier(); // for debugging reasons

    this.boundary =  new Rectangle();
    this.caption  = "";
    this.captionBoundary = new Rectangle();
    this.page = page;
}

Figure.prototype.setPage = function(page){
    this.page.removeFigure(this);
    this.page = page;
    this.page.addFigure(this);
};

Figure.prototype.remove = function(){
    this.page.removeFigure(this);
};

function Page(document){
    this.id = "Page" + getNextIdentifier();
    this.figures = [];

    this.image =  new Image("", 0, 0);
    this.minImage = new Image("", 0, 0);
    this.document = document;
}

/** Create a new figure belonging to the page
  */
Page.prototype.createNewFigure = function(){
    var figure = new Figure(this);
    this.addFigure(figure);
    return figure;
};

Page.prototype.addFigure = function(figure){
    this.figures.push(figure);
}

Page.prototype.removeFigure = function(figure){
    for (var figureInd in this.figures){
	if (this.figures[figureInd] == figure){
	    this.figures.splice(figureInd, 1);
	}
    }
};

Page.prototype.getFigures = function(){
    return this.figures;
}

/** A representation of the entire document */

function Document(){
    this.id = "Document" + getNextIdentifier();
    this.pages = []; // a collection of all pages belonging to the document
};


Document.prototype.createNewPage = function(){
    var newPage = new Page(this);
    this.pages.push(newPage);

    return newPage;
};

Document.prototype.getPages = function(){
    return this.pages;
};

Document.prototype.getPage = function(pageNum){
    return this.pages[pageNum];
};
