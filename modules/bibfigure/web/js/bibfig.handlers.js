var globalIdentifiersCounter = 0;
function getNextIdentifier(){
    globalIdentifiersCounter++;
    return globalIdentifiersCounter;
}

/**binding behaviour of the function*/

function prepareBoundHandler(callable, context){
    return function(){
        callable.apply(context, arguments);
    };
}

/** A simple imlementation of event handlers
    handlers can be registered and unregistered with names associated to them
*/

function EventHandler(){
    this.handlers = {};
}

/** Register a callback function or method the third optional argument
  * specifies in the context of which object the function should be called
  */
EventHandler.prototype.registerHandler = function(id, handler, context){
    context = context || this;
    this.handlers[id] = prepareBoundHandler(handler, context);
};

EventHandler.prototype.unregisterHandler = function(id){
    delete this.handlers[id];
};

EventHandler.prototype.invoke = function(arglist){
    for (handlerId in this.handlers){
        // the context does not matter here !
        handler = this.handlers[handlerId].apply(this, arglist);
    }
};

/** Invokes with one argument */
EventHandler.prototype.invokeOne = function(arg){
    this.invoke([arg]);
}



/** The events bus -> avery event of teh program passes here and can be interpreted by any element */

/** Each event is addressed by the event code and the identifier of the object 
  *  which is teh object of the operation. Objects are identifeid by their unique 
  *  string identifiers 
  *
  *  As the first argument of any event handler, the subjectId will be passed
  */
function EventsBus(){
    this.events = {};  // dictionary of events attached to the event itself

    this.objectEvents = {}; // dictionary of handlers attached to particular objects
    // eventId -> objectId -> handler

    this.universalHandler = new EventHandler();
}

EventsBus.prototype.registerUniversalHandler = function(id, handler, context){
    this.universalHandler.registerHandler(id, handler, context);
};

EventsBus.prototype.registerHandler = function(eventType, subscriberId, method,
    context, subjectId){
    if (subjectId == null || subjectId == undefined){
        if (this.events[eventType] == undefined){
            this.events[eventType] = new EventHandler();
        }
	
        this.events[eventType].registerHandler(subscriberId, method, context);
    } else {
        if (this.objectEvents[eventType] == undefined 
            || this.objectEvents[eventType] == null){
            this.objectEvents[eventType] = {};
        }
        if (this.objectEvents[eventType][subjectId] == undefined 
            || this.objectEvents[eventType][subjectId] == null){
            this.objectEvents[eventType][subjectId] = new EventHandler();
        }
        this.objectEvents[eventType][subjectId].registerHandler(subscriberId, 
            method, context);
    }
};

EventsBus.prototype.raise = function(eventType, subjectId, args){
    var newArgs = [subjectId].concat(args);
    // first executing handlers waiting for a particular event type without a 
    // distinction of objects
    if (this.events[eventType] != undefined){
        this.events[eventType].invoke(newArgs);
    } 
    if (this.objectEvents[eventType] != null && this.objectEvents[eventType] != undefined
        && this.objectEvents[eventType][subjectId] != null 
        && this.objectEvents[eventType][subjectId] != undefined){
        this.objectEvents[eventType][subjectId].invoke(newArgs);
    }
    // executing the universal handler
    this.universalHandler.invoke([eventType, subjectId, args]);
};

EventsBus.prototype.unregisterHandler = function(eventType, subscriberId, subjectId){
    if (subjectId == undefined || subjectId == null){
        if (this.events[eventType] != undefined){
            this.events[eventType].unregisterHandler(subsciberId);
        }
    } else {
        if (this.objectEvents[eventType] == undefined || this.objectEvents[eventType][subjectId] == undefined){
            alert("error. trying to unregister handler that has never been registered");
        }
        this.objectEvents[eventType][subjectId].unregisterHandler(subscriberId);
    }
};
