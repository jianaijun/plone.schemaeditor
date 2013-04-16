/*jslint white: true, onevar: true, undef: true, newcap: true, nomen: true,
  plusplus: true, bitwise: true, regexp: false, indent: 4 */

/*globals jQuery */

jQuery(function ($) {
    var editor = ace.edit("modelEditor"),
        session = editor.getSession(),
        myform = $("#saveform");

    // editor tuneup
    editor.setTheme("ace/theme/textmate");
    session.setMode("ace/mode/xml");
    session.setTabSize(4);
    session.setUseSoftTabs(true);
    session.setUseWrapMode(true);
    editor.setHighlightActiveLine(false);
    // Make save keystroke trigger save form submit
    editor.commands.addCommand({
        name: "save",
        bindKey: {win: "Ctrl-S", mac: "Command-S"},
        exec: function() {
            myform.submit();
        }
    });

    // enable save submit button on change
    session.on('change', function(e) {
        $('#saveform :submit').removeAttr('disabled');
    });

    // form submit handler; ajax posts data
    myform.on( "submit", function( event ) {
        var action = myform.attr('action');

        // prevent real submit
        event.preventDefault();

        // stuff the editor contents into the form
        // for easy serialization
        $('#savesource').val(editor.getValue());

        $.getJSON(action, myform.serialize(), function (rez) {
            if (rez.success) {
                var messagespan = $("#messagespan");

                // disable save button
                $('#saveform :submit').attr('disabled', 'disabled');
                messagespan.html(rez.message);
                messagespan.show().fadeOut(1000);


            } else {
                alert(rez.message);
            }
        })
        .fail(function() { alert("No response from server; not saved."); });

    });
});
