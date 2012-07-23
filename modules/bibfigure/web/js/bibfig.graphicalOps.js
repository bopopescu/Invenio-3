function getTransformedMargin(angle, scale, iwidth, iheight){
    var calcAngle = Math.PI * angle / 180;
    var width = Math.round(scale * iwidth);
    var height = Math.round(scale * iheight);

    var shx = 0;
    var shy = 0;


    if (angle >= 0  && angle <= 90){
        shx = height * Math.sin(calcAngle);
        shy = 0;
    }

    if (angle >= 90  && angle <= 180){
        shx = Math.sin(Math.PI - calcAngle) * height  + width * Math.cos(Math.PI - calcAngle);
        shy = Math.cos(Math.PI - calcAngle) * height;
    }

    if (angle >= -90  && angle <= 0){
        shx = 0;
        shy = - width * Math.sin(calcAngle);
    }

    if (angle >= -180 && angle <= -90){
        shx = Math.cos(Math.PI + calcAngle) * width;
        shy = Math.sin(Math.PI + calcAngle) * width + Math.cos(Math.PI + calcAngle) * height;
    }
    return {
        x: Math.round(shx),
        y: Math.round(shy)
    };
}

function getRealBoundary(width, height, angle){
    var radAngle = Math.PI * angle / 180;

    if (angle >= 0 && angle < 90){
        return {
            width: Math.round(Math.cos(radAngle) * width + Math.cos(Math.PI / 2 - radAngle) * height),
            height: Math.round(Math.cos(angle) * height + Math.cos(Math.PI / 2 - radAngle) * width)
        };
    }

    if (angle >= 90 && angle <= 180){
        return {
            width: Math.round(width * Math.cos(Math.PI - radAngle) + height * Math.sin(Math.PI - radAngle)),
            height: Math.round(width * Math.sin(Math.PI - radAngle) + height * Math.round( radAngle - Math.PI /2))
        };
    }

    if (angle < 0 && angle >= -90){
        return {
            height: Math.round( width * Math.sin(- radAngle) + height * Math.cos(Math.PI / 2 + radAngle)),
            width: Math.round( width * Math.cos(radAngle) - height * Math.sin(radAngle))
        };
    }

    if (angle < -90 && angle >= -180){
        var na = -radAngle - (Math.PI / 2);
        return {
            width: Math.round(height * Math.cos(na) + width * Math.sin(na)),
            height: Math.round(width * Math.cos(na) + height * Math.sin(na))
        };
    }

}


function buildTransformedCSS(tx, ty, scale, angle){
    return {
        "-moz-transform-origin" : "0 0",
        "-moz-transform": "translate(" + Math.round(tx) + "px, " + Math.round(ty) + "px) rotate(" + Math.round(angle) + "deg) scale("+ scale + ")",
        "-webkit-transform-origin" : "0 0",
        "-webkit-transform": "translate(" + Math.round(tx) + "px, " + Math.round(ty) + "px) rotate(" + Math.round(angle) + "deg) scale("+ scale + ")"
    }
}
function getTransformedCSS(angle, scale, iwidth, iheight){
    var trans = getTransformedMargin(angle, scale,
        iwidth, iheight);

    return buildTransformedCSS(trans.x, trans.y, scale, angle);
}




function toRadians(angle){
    return angle * (Math.PI / 180.);
}

/***
 * returns point translated by vector [tx; ty]
 * @param p dictionary with x and y entry
 * @param tx translation in x direction
 * @param ty translation in y direction
 * @return the translated point
 */
function translation(p, tx, ty){
    return {
        "x": p["x"] + tx, 
        "y": p["y"] + ty
    };
}

/***
 * returns point rotated by angle around the coordinate
 * center
 * @param p dictionary with x and y entry
 * @param angle angle in degrees to rotate with
 * @return the rotated point
 */
function rotation(p, angle){
    x = p["x"];
    y = p["y"];
    
    rangle = toRadians(angle)
    return {
        "x": Math.cos(rangle) * x - Math.sin(rangle) * y, 
        "y": Math.sin(rangle) * x + Math.cos(rangle) * y
    }
}