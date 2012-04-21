// stan 2012-02-04


function repeat(str, times) { 
    return new Array(times + 1).join(str);
}


// С итерацией и спойлером
function var_dump1(obj, tab) {
    if (typeof tab == "undefined")
        var tab = 0;

    var out = "";
    if(obj && typeof(obj) == "object") {
        if (tab > 2)
            return "*** прервано ***";

        if(!tab)
            out += "<pre>\n";
        out += '<a href="#" onClick="$(this).parent().children(\'span.object\').toggle();"><b>object {</b></a><span class="object">\n';

        for (var i in obj) {
            out += repeat("  ", tab) + "  " + i + ": ";
            if(typeof(obj[i]) == "object")
                out += var_dump1(obj[i], tab + 1);
            else
                out += obj[i];
            out += "\n";
        }

        out += repeat("  ", tab) + "</span>" + "<b>}</b>";
        if(!tab)
            out += "</pre>";
    } else
        out = repeat("  ", tab) + obj;

    if(!tab)
        out = out + "<br />\n";
    return out;
}


// Без итерации
function var_dump0(obj) {
    var out = "";
    if(obj && typeof(obj) == "object") {
        out += "<pre>\n";
        out += "<b>object {</b>\n";
        for (var i in obj) {
            out += "  " + i + ": ";
            out += obj[i];
            out += "\n";
        }
        out += "<b>}</b>\n";
        out += "</pre>\n";
    } else
        out = obj;

    return out;
}
