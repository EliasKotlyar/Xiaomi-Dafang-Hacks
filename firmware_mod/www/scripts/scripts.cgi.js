$(document).ready(function () {

    $("button.script_action_stop").click(function () {
        var e = $(this); console.log(e.prop("disabled"));
        if (!e.prop("disabled")) {
            e.prop("disabled", !e.prop("disabled"));
            e.addClass("is-loading");
            $.get(e.data("target")).done(function (res) {
                $("#show_" + e.data("script")).html(res);
                $("#content").load("/cgi-bin/scripts.cgi");
            });
        }
        return false;
    });

    $("button.script_action_start").click(function () {
        var e = $(this); console.log(e.prop("disabled"));
        if (!e.prop("disabled")) {
            e.prop("disabled", !e.prop("disabled"));
            e.addClass("is-loading");
            $.get(e.data("target")).done(function (res) {
                $("#show_" + e.data("script")).html(res);
                $("#content").load("/cgi-bin/scripts.cgi");
            });
        }
        return false;
    });

    $("input.autostart").click(function () {
        var e = $(this);
        e.prop("disabled", true);
        if (e.prop("checked")) {
            $.get(e.data("checked")).done(function (res) {
                e.prop("disabled", false);
                if (res.status == "ok") {
                    e.prop("checked", !e.prop("checked"));
                }
            });
        } else {
            $.get(e.data("unchecked")).done(function (res) {
                e.prop("disabled", false);
                if (res.status == "ok") {
                    e.prop("checked", !e.prop("checked"));
                }
            });
        }
        return false;
    });

    $(".view_script").click(function () {
        var e = $(this);
        var qv = $("#quickviewDefault");
        var v = $("#quicViewContent");
        if (qv.hasClass("is-active")) {
            // hide first if it's already active
            qv.toggleClass("is-active");
        }
        v.html("Loading...");
        v.load(e.attr("href"));
        qv.toggleClass("is-active");
        return false;
    });

});
