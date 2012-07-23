/** A general selector -> maintaining a list of elements, a current element
    parentElement -> where we want to insert the selector
  */
function Selector(eventsBus, parentElement, orientation){
    // claim your data
    if (orientation != "horizontal" && orientation != "vertical"){
	orientation = "horizontal";
    }

    this.id = "Selector" + getNextIdentifier();
    this.eventsBus = eventsBus;
    this.orientation = orientation;

    this.options = [];
    this.currentSelection = null;

    this.rootElement = $("<table  class=\"selectorRoot\"/>"); // this is ugly but seems to be the only non-dynamic way of doing this in this browser-like trojan called Internet Explorer
    if (this.orientation == "horizontal"){
	this.elementsContainer = $("<tr>");
	this.rootElement.append(this.elementsContainer);
    } else {
	this.elementsContainer = this.rootElement;
    }
    
    parentElement.append(this.rootElement);    
}

// events raised by this class
Selector.onSelectionChanged = "Selector.onSelectionChanged";


/**
  *  remove option from the selector
  */
Selector.prototype.removeOption = function(option){
    // remove link to it
    for (var optId in this.options){
	if (this.options[optId] == option){
	    this.options.splice(optId, 1);
	    break;
	}
    }
    
    this.eventsBus.unregisterHandler(SelectorOption.onSelected,
				     this.id,
				     option.id);

    // remove from the interface
    var uiElement = option.getRootUIElement();
    var toRemove = null;
    if (this.orientation == "horizontal"){
	toRemove = uiElement.parent();
    } else {
	toRemove = uiElement.parent().parent();
    }
    toRemove.remove();
    
    // change current selection if necessary
    if (this.currentSelection == option){
	this.onElementSelected(null, null); // remove current selection and 
	                               // notify others that it has changed
    }
}


/** add a new selector element */
Selector.prototype.addOption = function(option){
    this.eventsBus.registerHandler(
	SelectorOption.onSelected, 
	this.id, this.onElementSelected, 
	this, option.id);
    
    this.options.push(option);

    var wrapping = $("<td></td>");
    wrapping.append(option.getRootUIElement());
    var newElementRoot = null;
    if (this.orientation == "horizontal"){
	newElementRoot = wrapping;
    } else {
	newElementRoot = $("<tr></tr>");
	newElementRoot.append(wrapping);
    }
    this.elementsContainer.append(newElementRoot);
};


/** Event handler for the case of selection of one of subelements
  */

Selector.prototype.onElementSelected = function(eventSubject, newElement){
    if (newElement != this.currentSelection){
	this.currentSelection = newElement;
	this.eventsBus.raise(Selector.onSelectionChanged, this.id, 
			     [this.currentSelection]);
    }
};

/** option displayable in the selector */
function SelectorOption(eventsBus, selector){
    this.id = "SelectorOption" + getNextIdentifier();
    this.eventsBus = eventsBus;

    this.rootElement = $("<div class=\"selectorUnselectedOption\"/>");
    this.selector = selector;

    this.onMouseOn = new EventHandler();
    this.onMouseOff = new EventHandler();

    this.isSelected = false;

    this.rootElement.bind("click", prepareBoundHandler(this.onOptionClicked, this));
    this.rootElement.bind("mouseenter", prepareBoundHandler(this.onMouseEnterHandler, this));
    this.rootElement.bind("mouseleave", prepareBoundHandler(this.onMouseLeaveHandler, this));
    

    this.selector.addOption(this);
    this.eventsBus.registerHandler(Selector.onSelectionChanged, this.id, 
				   this.onSelectorSelectionChanged, this, selector.id);

    
    // we are going to listen to our own events and update the interface
    function onSelectedHandler(eventSubject){
	this.rootElement.removeClass("selectorUnselectedOption");
	this.rootElement.addClass("selectorSelectedOption");
    };
    
    function onDeselectedHandler(eventSubject){
	this.rootElement.addClass("selectorUnselectedOption");
	this.rootElement.removeClass("selectorSelectedOption");
    }
    
    function onHoveredHandler(){
	this.rootElement.addClass("selectorHoveredOption");
    }
    function onUnhoveredHandler(){
	this.rootElement.removeClass("selectorHoveredOption");
    }

    this.eventsBus.registerHandler(SelectorOption.onSelected, this.id, 
				  onSelectedHandler, this, this.id);

    this.eventsBus.registerHandler(SelectorOption.onDeselected, this.id,
				  onDeselectedHandler, this, this.id);

    
    this.onMouseOff.registerHandler(this.id, onUnhoveredHandler, this);
    this.onMouseOn.registerHandler(this.id, onHoveredHandler, this);
}

SelectorOption.onSelected = "SelectorOption.onSelected";
SelectorOption.onDeselected = "SelectorOption.onDeselected";

/**Select this option*/
SelectorOption.prototype.select = function(){
    if (!this.isSelected){
	this.isSelected = true;
	this.eventsBus.raise(SelectorOption.onSelected, this.id, [this])
    }
}
    
SelectorOption.prototype.onMouseLeaveHandler = function(){
    this.onMouseOff.invoke([]);
};

SelectorOption.prototype.onMouseEnterHandler = function(){
    this.onMouseOn.invoke([]);
};


SelectorOption.prototype.getRootUIElement = function(){
    return this.rootElement;
};

/** A handler of the event of clicking the option */
SelectorOption.prototype.onOptionClicked = function(){
    // mark this element as selected
    this.select();
};

/** react to the event of changing the selection inside the selector
  */
SelectorOption.prototype.onSelectorSelectionChanged = function(subjectId, newSelection){
    if (newSelection !== this && this.isSelected){
	this.isSelected = false;
	this.eventsBus.raise(SelectorOption.onDeselected, this.id, [this]);
//	this.onDeselected.invokeOne(this);a
    } 
};

/** puts a particular content into the selector place-holder
*/
SelectorOption.prototype.setContent = function(content){
    this.rootElement.append(content);
};
