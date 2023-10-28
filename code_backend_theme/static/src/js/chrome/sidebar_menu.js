odoo.define('code_backend_theme.SidebarMenu', function (require) {
    "use strict";

    //sidebar toggle effect
    $(document).on("click", "#closeSidebar", function(event){
        $("#closeSidebar").hide();
        $("#openSidebar").show();
    });
    $(document).on("click", "#openSidebar", function(event){
        $("#openSidebar").hide();
        $("#closeSidebar").show();
    });
    $(document).on("click", "#openSidebar", function(event){
        $("#sidebar_panel").css({'display':'block', 'width': '200px'});
        $(".sidebar_close").css({'display':'none'});
        $(".sidebar_logo").css({'display':'block'});
        $(".sidebar_head").css({'padding-top':'20px'});
        $(".sidebar_img").css({'width':'20px'});
        $(".sidebar_img").css({'margin-right':'8px'});
        $(".sidebar_app_name").css({'display':'block'});
        

        //add class in navbar
        var navbar = $(".o_main_navbar");
        var navbar_id = navbar.data("id");
        $("nav").addClass(navbar_id);
        navbar.addClass("small_nav");

        //add class in action-manager
        var action_manager = $(".o_action_manager");
        var action_manager_id = action_manager.data("id");
        $("div").addClass(action_manager_id);
        action_manager.addClass("sidebar_margin");

        //add class in top_heading
        var top_head = $(".top_heading");
        var top_head_id = top_head.data("id");
        $("div").addClass(top_head_id);
        top_head.addClass("sidebar_margin");
    });
    $(document).on("click", "#closeSidebar", function(event){
        $("#sidebar_panel").css({'width': '100px'});
        $(".sidebar_close").css({'display':'block'});
        $(".sidebar_logo").css({'display':'none'});
        $(".sidebar_head").css({'padding-top':'30px'});
        $(".sidebar_img").css({'width':'50px'});
        $(".sidebar_app_name").css({'display':'none'});

        //remove class in navbar
        var navbar = $(".o_main_navbar");
        var navbar_id = navbar.data("id");
        $("nav").removeClass(navbar_id);
        navbar.removeClass("small_nav");

        //remove class in action-manager
        var action_manager = $(".o_action_manager");
        var action_manager_id = action_manager.data("id");
        $("div").removeClass(action_manager_id);
        action_manager.removeClass("sidebar_margin");

        //remove class in top_heading
        var top_head = $(".top_heading");
        var top_head_id = top_head.data("id");
        $("div").removeClass(top_head_id);
        top_head.removeClass("sidebar_margin");
    });

    $(document).on("click", ".sidebar a", function(event){
        var menu = $(".sidebar a");
        var $this = $(this);
        var id = $this.data("id");
        $("header").removeClass().addClass(id);
        menu.removeClass("active");
        $this.addClass("active");

        
        //remove class in navbar
        var navbar = $(".o_main_navbar");
        var navbar_id = navbar.data("id");
        $("nav").removeClass(navbar_id);
        navbar.removeClass("small_nav");

        //remove class in action-manager
        var action_manager = $(".o_action_manager");
        var action_manager_id = action_manager.data("id");
        $("div").removeClass(action_manager_id);
        action_manager.removeClass("sidebar_margin");

        //remove class in top_heading
        var top_head = $(".top_heading");
        var top_head_id = top_head.data("id");
        $("div").removeClass(top_head_id);
        top_head.removeClass("sidebar_margin");
    });
});