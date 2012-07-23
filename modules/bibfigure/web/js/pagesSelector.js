/**PagesSelector class -> choose the current page from the list of page miniatures
  * container: a layer that will be transformed into a pages selector
  */

function PagesSelector(container, eventsBus, document, entryWidth, entryHeight){
    this.id = "PagesSelector" + getNextIdentifier();
    this.eventsBus = eventsBus;
    this.internalEventsBus = new EventsBus();

    // claim your data
    this.document = document;
    this.entryWidth = entryWidth;
    this.entryHeight = entryHeight;

    // claim your interface
    this.rootUIElement = container;
    this.selectorPlaceholder = $("<div></div>");
    this.rootUIElement.append(this.selectorPlaceholder);
    this.selector = new Selector(this.internalEventsBus, 
				 this.selectorPlaceholder, "vertical");

    this.pagesToOptions = {};

    // adding interface for all the document pages ! 
    //   (pages are static -> once read, they do not change)

    this.createSelector();
    
    this.eventsBus.registerHandler(Presenter.setPage, this.id, 
				   function(subjectId, page){
				       this.setPage(page);
				   }, this)
}

PagesSelector.onPageSelected = "PagesSelector.onPageSelected";


PagesSelector.prototype.getRootUIElement = function(){
    return this.rootUIElement;
};

PagesSelector.prototype.createNewPageController = function(page){
    var view = new PageView(this.internalEventsBus, page, this.entryWidth,
			    this.entryHeight);
    var selectorOption = new SelectorOption(this.internalEventsBus, this.selector);
    selectorOption.setContent(view.getRootUIElement());
    
    this.internalEventsBus.registerHandler(
	SelectorOption.onSelected, this.id, 
	function(eventSubject){
	    this.eventsBus.raise(PagesSelector.onPageSelected, this.id, [page]);
	}, this, selectorOption.id);
    this.pagesToOptions[page.id] = selectorOption;
};

PagesSelector.prototype.setPage = function(newPage){
    this.pagesToOptions[newPage.id].select();
};

//TODO: this function should clean the pages collection before proceeding
//      for the time being, we just assume it is called on a complete document
PagesSelector.prototype.createSelector = function(){
    var pages = this.document.getPages();
    for (var pageId in pages){
	this.createNewPageController(pages[pageId]);
    }
}



/**
  * a widget allowing to display page - somehow simpler than with figures as pages 
  * do not change
  */
function PageView(eventsBus, page, maxWidth, maxHeight){
    this.eventsBus = eventsBus;
    this.pageDisplay = new ImageView(this.eventsBus, page.minImage);
    this.maxWidth = maxWidth;
    this.maxHeight = maxHeight;
    this.boundary = new Rectangle(0, 0, maxWidth, maxHeight);
    this.pageDisplay.draw(new Rectangle(0, 0, page.minImage.width, page.minImage.height), 
			  this.boundary, 0, true, false);
}

PageView.prototype.getRootUIElement = function(){
    return this.pageDisplay.getRootUIElement();
};

