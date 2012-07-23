function BusLogger(eventsBus){
    this.rootElement = $("#eventsBusLog");
    this.eventsBus = eventsBus;
    this.eventsBus.registerUniversalHandler("bus logger", function(eventName, eventSubject, eventArgs){
	var newElement = $("<div style=\"display: table-row; border-width: 5px; border-color:white; border-style:solid;\"><div style=\"display: table-cell;\">" + eventName + "</div>" 
			   + "<div style=\"display: table-cell; border-width: 5px; border-color:white; border-style:solid;\">" + eventSubject + "</div>"
			   + "<div style=\"display: table-cell; border-width: 5px; border-color:white; border-style:solid;\">" + eventArgs + "</div></div>");
	this.rootElement.append(newElement);
    },this);
}
