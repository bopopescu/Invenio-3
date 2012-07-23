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
    metaurl = '/record/'+recid+'/pageimages/meta-info';
    if(approvalid > 0){
        metaurl += '?approve=' + approvalid;
        $("#btnSave").css('display', 'none');
    }
    else{
        $("#btnApprove").css('display', 'none');
    }
    $.getJSON(metaurl, function(data) {
        if("error" in data){
            alert("There was an error while loading the pdf: " + data['error']);
            return;
        }

        for (var pageNum = 0; pageNum < parseInt(data['pages']); pageNum++){
            var newPage = pdfDocument.createNewPage();
            
            pageResolution = data['pageResolution'][pageNum].split(",");
            pWidth = parseFloat(pageResolution[0])
            pHeight = parseFloat(pageResolution[1])
            
            // scale down to 560 width
            scale = 560. / pWidth
            scaledHeight = parseInt(scale*pHeight);
            newPage.image = new Image("/record/"+recid+"/pageimages/" + pageNum, 560, scaledHeight);
            newPage.image.onerror = function(source){
                alert('lol')
            }
            newPage.minImage = new Image("/record/"+recid+"/pageimages/" + pageNum, 137, parseInt((137. / pWidth)*pHeight));
            eventsBus.raise(Presenter.pageCreated, "presenter", [newPage]);
        }
        var currentPage = pdfDocument.getPage(0);
        var currentFigure = null;
        
        var i = 1;
        while("figure"+i in data){
            figBoundaryData = data["figure"+i]["location"]["boundary"];
            captBoundaryData = data["figure"+i]["caption_location"]["boundary"];
            figResolution = data["figure"+i]["location"]["page_resolution"]
            captResolution = data["figure"+i]["caption_location"]["page_resolution"]
            
            figScale = (560./figResolution["width"]);
            captScale = (560./captResolution["width"])

            // new figure boundary objects
            var fig = pdfDocument.createFigure()
            var figBoundary = new Boundary();
            figBoundary.setRectangle(new Rectangle(parseInt(figBoundaryData["x"] * figScale), 
                parseInt(figBoundaryData["y"] * figScale), 
                parseInt(figBoundaryData["width"] * figScale), 
                parseInt(figBoundaryData["height"] * figScale),
                parseFloat(figBoundaryData["alpha"]))); //angle
            figBoundary.setPage(pdfDocument.getPage(parseInt(data["figure"+i]["location"]["page_num"])))
            fig.setFigureBoundary(figBoundary);
            
            var captBoundary = new Boundary();
            captBoundary.setRectangle(new Rectangle(parseInt(captBoundaryData["x"] * captScale), 
                parseInt(captBoundaryData["y"] * captScale), 
                parseInt(captBoundaryData["width"] * captScale), 
                parseInt(captBoundaryData["height"] * captScale),
                parseFloat(captBoundaryData["alpha"]))); //angle
            captBoundary.setPage(pdfDocument.getPage(parseInt(data["figure"+i]["caption_location"]["page_num"])))
            fig.setCaptionBoundary(captBoundary);
            fig.setCaption(data["figure"+i]["caption"])
            //eventsBus.raise(Presenter.figureCreated, "presenter", [fig]);
            i++;
        }
        
        var pageView = new PageViewArea($("#pageViewArea"), eventsBus);
        var figureControls = new  FigureControlsArea(eventsBus, pdfDocument, pageView);

        eventsBus.registerHandler(
            FigureControlsArea.onFigureBoundarySelected,
            "presenter", function(subjectId, selection){
                if (currentFigure.getFigureBoundary().page != currentPage){
                    currentFigure.getFigureBoundary().setPage(currentPage)
                }

                currentFigure.getFigureBoundary().setRectangle(new Rectangle(selection.x,
                    selection.y,
                    selection.width,
                    selection.height,
                    selection.angle));

                eventsBus.raise(Presenter.figureChanged, currentFigure.id, [currentFigure]);

            }, this, figureControls.id);


        eventsBus.registerHandler(
            FigureControlsArea.beforeFigureCaptionSelection, "presenter",
            function(subjectId){
            //put stuff here if you want
            }, this, figureControls.id);

        eventsBus.registerHandler(
            FigureControlsArea.onFigureCaptionSelected , "presenter",
            function(subjectId, selection){
                if (currentFigure.getCaptionBoundary().page != currentPage){
                    currentFigure.getCaptionBoundary().setPage(currentPage)
                }
                currentFigure.getCaptionBoundary().setRectangle(new Rectangle(selection.x,
                    selection.y,
                    selection.width,
                    selection.height,
                    selection.angle));
                eventsBus.raise(Presenter.figureChanged, currentFigure.id, [currentFigure]);
            }, this, figureControls.id);

        var figuresSelector = new FiguresSelector($("#figuresSelector"), eventsBus, pdfDocument, 100, 100);

        eventsBus.registerHandler(
            FiguresSelector.onFigureSelected, "presenter",
            function(subjectId, figure){
                currentFigure = figure;
                eventsBus.raise(Presenter.setFigure, "presenter", [figure]);
            }, figuresSelector.id);

        figuresSelector.onCreateNewFigure.registerHandler("presenter", function(){
            if (currentPage != null && currentPage != undefined){
                var newFigure = currentPage.pdfDocument.createFigure(currentPage);
                currentFigure = newFigure;
                eventsBus.raise(Presenter.figureCreated, "presenter", [newFigure]);
                eventsBus.raise(Presenter.setFigure, "presenter", [newFigure]);
            } else {
                alert("Trying to create a figure not attached to a page");
            }
        }, this);

        //dealing with the list of pages
        var pageSelector = new PagesSelector($("#pagesSelectorLayer"),
            eventsBus, pdfDocument, 150, 200);

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
            }, this, figureControls.id);
            
        eventsBus.registerHandler(FigureControlsArea.onSaveClicked,
            "presenter", function(){
                if(confirm("Have you finalized your edits? ")){
                    var jfigs = pdfDocument.getFiguresJSON();
                    $.post('/record/'+recid+'/pageimages/meta-info-save', 
                    {
                        "jsondata": JSON.stringify(jfigs)
                    }, function(data){
                        alert("A request for your update has been successfully saved. ");
                    },
                    'html'
                    );
                }
            }, this, figureControls.id);
            
        eventsBus.registerHandler(FigureControlsArea.onApproveClicked,
            "presenter", function(){
                if(confirm("Have you finalized your edits and are ready to approve the submission? ")){
                    var jfigs = pdfDocument.getFiguresJSON();
                    jfigs["approvalid"] = approvalid;
                    $.post('/record/'+recid+'/pageimages/meta-info-save', 
                    {
                        "jsondata": JSON.stringify(jfigs)
                    }, function(data){
                        alert("Approval successfully saved. ");
                    },
                    'html'
                    );
                }
            }, this, figureControls.id);
            
            
        eventsBus.registerHandler(FigureControlsArea.onExtractCaptionClicked,
            "presenter", function(subjectId, figure){
                page = figure.getCaptionBoundary().page
                rect = figure.getCaptionBoundary().rectangle;
              
                // do calculations according to css calculations for 
                // viewing the boxes if the page is rotated
                // assume scale = 1 and viewAngle = 0
                var tm1 = getTransformedMargin(rect.angle,
                    1., page.image.width, page.image.height);

                var tm2 = getTransformedMargin(0., 1., page.image.width, page.image.height);

                points = new Array(4);
                // points in draw direction
                points[0] = {
                    "x": rect.x, 
                    "y": rect.y
                };
                
                points[1] = {
                    "x": rect.x+rect.width, 
                    "y": rect.y
                };
                
                points[2] = {
                    "x": rect.x+rect.width, 
                    "y": rect.y+rect.height
                };
                
                points[3] = {
                    "x": rect.x, 
                    "y": rect.y+rect.height
                };
                jsonreq = {}
                // translate points according to the css translations
                for(var i = 0; i < 4; i++){
                    
                    p = points[i]
                
                    p = translation(p, tm2.x, tm2.y);
                    p = rotation(p, -rect.angle);
                
                    s = {
                        "x": -tm1.x, 
                        "y": -tm1.y
                    }

                    s = rotation(s, -rect.angle)
                    p = translation(p, s["x"], s["y"])
                    jsonreq["p"+i] = p['x']+", "+p["y"];
                }
                
                jsonreq['page'] = page.getNumber();
                
                $.post('/record/'+recid+'/pageimages/extract-caption', 
                {
                    "jsondata": JSON.stringify(jsonreq)
                }, function(data){
                    
                    if(confirm("Do you want to store the extracted caption?\n\nCaption: "+data['caption'])){
                        figure.setCaption(data['caption']);
                        $("#figureCaptionText").val(data['caption']);
                    }
                },
                'json'
                );
            }, this, figureControls.id);

        
        // now create initial data view
        // TODO: this code is temporary !
        for (var figureId in pdfDocument.getFigures()){
            currentFigure = pdfDocument.figures[figureId];
            eventsBus.raise(Presenter.figureCreated, "presenter",
                [pdfDocument.figures[figureId]]);
            
        }
        eventsBus.raise(Presenter.setPage, "presenter", [currentPage]);
        eventsBus.raise(Presenter.setFigure, "presenter", [currentFigure]);
    });
});
