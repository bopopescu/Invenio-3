/**A class providing a plot preview with a selected scale.
   This class does not use HTML for templating as there might 
   be more image previews on the page*/

function ImageView(eventsBus, image, container){
    // claim my data
    this.eventsBus = eventsBus;
    // preparing the interface
    this.element = $('<div class="imageRegionPreviewBnd"/>');
    this.imagePositioner = $('<div class="imageRegionPreview"/>');
    var url = image ? image.getUrl(): "";
    this.imageElement =  $('<img src="' + url + '" class="imageRegionPreviewImg"/>');

    this.image = image;
    
    if (container != undefined){
        container.append(this.element);
    }

    this.element.append(this.imagePositioner);
    this.imagePositioner.append(this.imageElement);
}

ImageView.prototype.getRootUIElement = function(){
    return this.element;
};

ImageView.prototype.setImage = function(image){
    this.image = image;
    if (image != undefined && image != null){
        this.imageElement.attr("src", image.getUrl());
    }
};

/** draw a selected region of the image so that it takes at maximum a givyen space 
  * What is happening effectively:
  *        width1
  *    -------------    
  *   |             |
  *   |(x1,y1)      |h       width2
  *   |     #####   |e        -------- 
  *   |     #####   |i       | (x2,y2)|h
  *   |     #####h  |g       |    ##h |e
  *   |     #####1  |h   ->  |    ##2 |i
  *   |     #####   |t       |    ##  |g
  *   |      w1     |1       |    w2  |h
  *   |             |         -------- t
  *    -------------                   2
  *  
  * (x1, y1) - coordinates of the beginning of the rectangle in the first image
  * (width1, height1) - dimensions of the original image
  * (w1, h1) - dimensions of the original image
  *
  * the function calculates (width2, height2) and (x2,y2)
  * based on values of (w1,h1), (w2, h2), (width1, height1), (x1, y1)
  * The proportions between rectangles are preserved)
  *
  * Parameters:
  *   area - area of the original image that should be drawn
  *   view - a rectangle whose width and height specify the maximal boundary
  *   extendH - should the box be extended horizontally to fill view ?
  *   extendV - should the box be extended vertically to fill view ?
  */ 
ImageView.prototype.draw = function(area, view, extendH, extendV ){ 
    extendH = extendH || true;
    extendV = extendV || false;

    var scale = (area.width == 0 || area.height == 0) ? 1 
    : area.getFittingScale(view);
    

    //scale is expressed as new/old
    var effWidth = Math.round(area.width * scale);
    var effHeight = Math.round(area.height * scale);

    var effImgWidth = this.image ? Math.round(this.image.width * scale) : 0;
    var effImgHeight = this.image ? Math.round(this.image.height * scale) : 0;
    var effPosX = Math.round(area.x * scale);
    var effPosY = Math.round(area.y * scale);

    // parameters allowing to embed the image in a bounding box
    var effBndWidth = extendH ? view.width : effWidth;
    var effBndHeight = extendV ? view.height : effHeight;
    var effX = extendH ? Math.round((view.width - effWidth) / 2) : 0;
    var effY = extendV ? Math.round((view.height - effHeight) / 2) : 0;
    
    this.element.css({
        display: "inline-block",
        width: effBndWidth + "px",
        height: effBndHeight + "px",
        maxWidth: effBndWidth + "px",
        maxHeight: effBndHeight + "px",
        overflow: "hidden"
    });
    
    this.imagePositioner.css({
        display: "inline-block",
        width: effWidth + "px",
        height: effHeight + "px",
        position: "relative",
        overflow: "hidden",
        top: effY + "px",
        left: effX + "px"
    });

    this.imageElement.css({
        width: effImgWidth + "px",
        height: effImgHeight + "px",
        marginLeft: "-" + effPosX + "px",
        marginTop: "-" + effPosY + "px"
    });     
};

