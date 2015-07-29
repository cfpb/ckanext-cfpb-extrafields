//<!-- http://stackoverflow.com/questions/9154026/jquery-dynamically-load-a-gist-embed -->

function adjustIframeSize(newHeight) {
    var i = document.getElementById("gistFrame");
    i.style.height = parseInt(newHeight) + "px";
}

$("#resource-gists .resource-gist").each(function(){
    if ($(this).data('gist-url')) {
        // Create an iframe, append it to this document where specified
        var gistFrame = document.createElement("iframe");
        gistFrame.setAttribute("width", "100%");
        gistFrame.id = "gistFrame";
        
        var zone = document.getElementById("gistZone");
        zone.innerHTML = "";
        zone.appendChild(gistFrame);
        
        // Create the iframe's document
        var gistFrameHTML = '<html><body onload="parent.adjustIframeSize(document.body.scrollHeight)"><scr'+'ipt type="text/javascript" src="' + $(this).data('gist-url') + '.js"></sc'+'ript></b'+'ody></h'+'tml><base target="_parent" />';

        // Set iframe's document with a trigger for this document to adjust the height
        var gistFrameDoc = gistFrame.document;
        
        
        if (gistFrame.contentDocument) {
            gistFrameDoc = gistFrame.contentDocument;
        } else if (gistFrame.contentWindow) {
            gistFrameDoc = gistFrame.contentWindow.document;
        }
        
        gistFrameDoc.open();
        gistFrameDoc.writeln(gistFrameHTML);
        gistFrameDoc.close();
    }
});

$('.expandable').expandable();
console.log(98798798)
