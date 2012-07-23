/**
 *A class displaying fractions
 */


function FractionDisplay(container, unit){
    this.mainElement = null;
    this.unit = unit;
    this.container = container;


    this.mainElement = $("<table><tr><td rowspan=\"2\" class=\"sign\">==</td><td style=\"border-bottom: 1px; border-top: 0; border-left: 0; border-right: 0; border-color: black; border-style: solid;\" class=\"delimiter\">0</td><td rowspan=\"2\" class=\"unit\">" + this.unit + "</td></tr><tr><td class=\"divisor\">0</td></tr></table>");
    this.mainSingleElement = $("<div style=\"position: absolute; bottom: 10px;\">0</div>");

    this.delElement = this.mainElement.find(".delimiter");
    this.divElement = this.mainElement.find(".divisor");
    this.unitElement = this.mainElement.find(".unit");
    this.signElement = this.mainElement.find(".sign");

    this.mainElement.show();
    this.mainSingleElement.hide();
    this.container.append(this.mainElement);
    this.container.append(this.mainSingleElement);
    this.setNumber(0, 0);
}


FractionDisplay.prototype.gcd = function(a, b){
    if (b < 0){
	return this.gcd(a, -b);
    }

    if (a < 0){
	return this.gcd(-a, b);
    }

    if (b > a){
	return this.gcd(b, a);
    }

    if (b == 0){
	return a;
    } else {
	return this.gcd(b, a % b);
    }
};

FractionDisplay.prototype.setNumber = function(del, div){
    // finding greatest common dividor
    var gcd = this.gcd(del, div);
    var ndel = 0;
    var ndiv = 0;
    var nsign = "";

    if (gcd != 0){
	ndel = Math.abs(del / gcd);
	ndiv = Math.abs(div / gcd);
	nsign = (del * div < 0) ? "-" : "";
    }

//    if (this.mainElement != null){
//	this.mainElement.remove();
//    }

    if (ndel == 0){
	// we are zero ! -> display zero and hide the
	//this.mainElement = $("<p>0</p>");
	//this.container.append(this.mainElement);
	this.mainSingleElement.html("0");
	this.mainSingleElement.show();
	this.mainElement.hide();

	return;
    }

    if (ndiv == 1){
	// display a non-fraction
//	this.mainElement = $("<p>">ndel + this.unit + "</p>");
//	this.container.append(this.mainElement);
	this.mainSingleElement.html(nsign + (ndel == 1 ? "" : ndel) + this.unit);
	this.mainSingleElement.show();
	this.mainElement.hide();

	return;
    }
    this.delElement.html(ndel);
    this.divElement.html(ndiv);
    this.unitElement.html(this.unit);
    this.signElement.html(nsign);
    this.mainSingleElement.hide();
    this.mainElement.show();

    // normal case
//    this.mainElement = $("<table><tr><td style=\"border-bottom: 1px; border-top: 0; border-left: 0; border-color: black; border-style: dotted;\">" + ndel+ "</td><td rowspan=\"2\">" + this.unit + "</td></tr><tr><td>" + ndiv + "</td></tr></table>");
  //  this.container.append(this.mainElement);

};