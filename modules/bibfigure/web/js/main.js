/** For the testing purposes, we do not want to have backend yet ...
  *  we create a sample data here. Later this will be generated
  *  automatically by server-side scripts
  */

/*function createSampleDocument(eventsBus){
    var document = new Document();
    for (var pageNum = 0; pageNum < 12; pageNum++){
	var newPage = document.createNewPage();
	newPage.image = new Image("data/" + pageNum + ".png", 612, 792);
	newPage.minImage = new Image("data/min/" + pageNum + ".png", 150, 194);
	eventsBus.raise(Presenter.pageCreated, "presenter", [newPage]);
    }

    // now creating sample figures

    var f1 = document.getPage(2).createNewFigure();
    f1.boundary = new Rectangle(118, 74, 374, 262);
    f1.captionboundary = new Rectangle(63, 337, 488, 43);

    var f2 = document.getPage(3).createNewFigure();
    f2.boundary = new Rectangle(161, 276, 298, 220);
    f2.captionboundary = new Rectangle(70, 494, 479, 44);

    return document;
}
*/



/** the main presenter class
 */
function Presenter(){
}

/* events of the presenter -> they are interpreted by elements of the interface */
Presenter.setPage = "setPage";
Presenter.setFigure = "setFigure";
Presenter.disableInterface = "disableInterface";
Presenter.deletedFigure = "deletedFigure";
Presenter.figureCreated = "createdFigure";
Presenter.figureChanged = "changedFigure";
Presenter.pageCreated = "createdPage";
Presenter.figureRemoved = "figureRemoved";

$(document).ready(function () {
    var eventsBus = new EventsBus();
//    var document = createSampleDocument(eventsBus);
    var document = createDocumentFromSampleData(eventsBus);
    var currentPage = document.getPage(0);
    var currentFigure = null;

    var pageView = new PageViewArea($("#pageViewArea"), eventsBus);
    var plotControls = new  FigureControlsArea(eventsBus, pageView);

    eventsBus.registerHandler(
	FigureControlsArea.onFigureBoundarySelected,
	"presenter", function(subjectId, selection){
	    if (currentFigure.page != currentPage){
		currentFigure.setPage(currentPage)
		currentFigure.captionBoundary = new Rectangle(0, 0, 0, 0);
	    }

	    currentFigure.boundary = new Rectangle(selection.x,
						   selection.y,
						   selection.width,
						   selection.height,
						   selection.angle);

	    eventsBus.raise(Presenter.figureChanged, currentFigure.id, [currentFigure]);

	}, this, plotControls.id);


    eventsBus.registerHandler(
	FigureControlsArea.beforeFigureCaptionSelection, "presenter",
	function(subjectId){
	    if (currentPage != currentFigure.page){
		// when selecting the caption, we want the page to be set
		// to the figure page

		currentPage = currentFigure.page;
		eventsBus.raise(Presenter.setPage, "presenter", [currentPage]);
	    }
	}, this, plotControls.id);

    eventsBus.registerHandler(
	FigureControlsArea.onFigureCaptionSelected , "presenter",
	function(subjectId, selection){
	    currentFigure.captionBoundary = new Rectangle(selection.x,
							  selection.y,
							  selection.width,
							  selection.height);
	    eventsBus.raise(Presenter.figureChanged, currentFigure.id, [currentFigure]);
	}, this, plotControls.id);

    var figuresSelector = new FiguresSelector($("#figuresSelector"), eventsBus, document, 100, 100);

    eventsBus.registerHandler(
	FiguresSelector.onFigureSelected, "presenter",
	function(subjectId, figure){
	    currentFigure = figure;
	    eventsBus.raise(Presenter.setFigure, "presenter", [figure]);
	}, figuresSelector.id);

    figuresSelector.onCreateNewFigure.registerHandler("presenter", function(){
	if (currentPage != null && currentPage != undefined){
	    var newFigure = currentPage.createNewFigure();
	    currentFigure = newFigure;
	    eventsBus.raise(Presenter.figureCreated, "presenter", [newFigure]);
	    eventsBus.raise(Presenter.setFigure, "presenter", [newFigure]);
	} else {
	    alert("Trying to create a figure not attached to a page");
	}
    }, this);

    //dealing with the list of pages
    var pageSelector = new PagesSelector($("#pagesSelectorLayer"),
					 eventsBus, document, 150, 200);

    eventsBus.registerHandler(PagesSelector.onPageSelected,
			      "global", function(subjectId, page){
				  currentPage = page;
				  eventsBus.raise(Presenter.setPage,
						  "presenter", [page]);
			      });

    eventsBus.registerHandler(FigureControlsArea.onRemoveFigureClicked,
			      "presenter", function(subjectId, figure){
				  eventsBus.raise(Presenter.figureRemoved,
						  "presenter",
						  [figure]);
				  figure.remove();
				  eventsBus.raise(Presenter.setFigure,
						  "presenter",
						  [null]);
			      }, this, plotControls.id);

    new BusLogger(eventsBus);


    // now create initial data view
// TODO: this code is temporary !
    var currentFigure = null;
    for (var pageId in document.getPages()){
	var page = document.getPage(pageId);
	for (var figureId in page.getFigures()){
	    currentFigure = page.figures[figureId];
	    eventsBus.raise(Presenter.figureCreated, "presenter",
			    [page.figures[figureId]]);
	}
    }

//    eventsBus.raise(Presenter.figureCreated, "presenter", [document.getPage(3).figures[0]])

    eventsBus.raise(Presenter.setPage, "presenter", [currentPage]);


    eventsBus.raise(Presenter.setFigure, "presenter", [currentFigure]);

    // We transform our interface elements into areas that can be detached as floating windows !
    /*
    var winSelectPage = new Windowifyer(pageSelector.getRootUIElement(),
					"Page selection", "horizontal");
    var winSelectFigure = new Windowifyer(figuresSelector.getRootUIElement(),
					  "figures selection", "horizontal");
    var winFigureControls = new Windowifyer(plotControls.getRootUIElement(),
					    "Current figure controls", "horizontal");
    var winPageView = new Windowifyer(pageView.getRootUIElement(),
				      "Page preview", "horizontal", "ui-pageviewarea-windowified");

    $("#exampleDiv").dialog({height: 400});
    $("#exampleDiv2").dialog({height: 300});
*/
});
