$(document).ready(function() {
    $("#value1").focus();
});

valueList = $(".value")

$("form div input").keyup(function () {
    for (i=0;i<valueList.length;i ++) {
        if (this.value.length == 1) {
            $(this).next().focus();
        }
    }
});

