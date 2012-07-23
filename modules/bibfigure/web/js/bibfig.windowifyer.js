
/**
  *A widget exposing an interface for detachment of a given frame as a window or hiding it
  */

function Windowifyer(parent, title, orientation, windowifiedClass){
    orientation = orientation || "horizontal";
    
    this.windowifiedClass= windowifiedClass || "ui-windowify-windowedcontent";
    
    this.parent = parent;

    this.mainElement = $("<div class=\"ui-windowify-controltoolbar\"></div>");
    this.parent.prepend(this.mainElement);

    this.hideControl = $("<input type=\"button\" value=\"hide\"></input>");
    this.mainElement.append(this.hideControl);
    this.windowifyControl = $("<input type=\"button\" value=\"make a window\"></input>");
    this.mainElement.append(this.windowifyControl);
    
    this.windowifyControl.bind("click", 
			       prepareBoundHandler(this.onMakeWindowClicked, this));
    this.hideControl.bind("click", 
			       prepareBoundHandler(this.onHideClicked, this));
    this.title = title;
    
}

Windowifyer.prototype.onMakeWindowClicked = function(){
    this.parent.wrap("<div></div>");
    this.parent.parent().dialog({
	height: this.parent.height(),
	width: this.parent.width(),
	title: this.title
    });
    this.parent.addClass(this.windowifiedClass);
};

Windowifyer.prototype.onHideClicked = function(){
    this.parent.addClass("ui-windowify-hiddencontent");
};

