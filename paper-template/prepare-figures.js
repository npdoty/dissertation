var margin = {top: 30, right: 30, bottom: 30, left: 30},
width = 960 - margin.left - margin.right,
height = 350 - margin.top - margin.bottom;

function prepareFigures() {
  var figureImg = $("figure img");
  figureImg.each(function() {
    var graphName = $(this).attr("src").split("/")[1].split(".svg")[0];
    $(this).parent("figure").attr("id", graphName);
    
    if (generatedFigures.indexOf(graphName) != -1) {
      $(this).remove();
    }
  });
}

function createSidenotes() {
  var $markers = $('.footnoteRef');
  var $footnotes = $('section.footnotes ol');
  var $footnoteArray = $footnotes.children();

  $markers.parent().wrap("<div class='post-subject'></div>");

  for (var i = 0; i < $markers.length; i++) {
      $($('.post-subject')[i]).append(
          // role='complementary' provided for ARIA support
          "<aside class='post-sidenote' role='complementary'>"
          + $($footnoteArray[i]).html()
          + "</aside>"
      );
  }
}

function toggleNotes() {
  var $markers = $('.footnoteRef');
  var $footnotes = $('section.footnotes ol');
  if ($footnotes.length > 0 && $markers.length > 0) {
      $('body').addClass('has-sidenotes');
  }
}

function prepareAnnotations() {
  $('<p></p>').html("Optionally, you can highlight and comment directly on this web page with an <a href=\"http://annotateit.org/\">AnnotateIt</a> account: <a href=\"#\">enable annotation</a>.").appendTo("#sotd");
  
  $('a:contains("enable annotation")').click(function(){
    $('body').annotator().annotator('setupPlugins', {}, {Filter: false});
    return false;
  });
}