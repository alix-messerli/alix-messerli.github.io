var app = (function(){
    let pages = [];
    let links = [];
    let currentIndex = 0;
    let root_vars = "";

    document.addEventListener("DOMContentLoaded", function(){
        root_vars = document.querySelector(':root');
        pages = document.querySelectorAll('[data-page]');
        links = document.querySelectorAll('[data-role="link"]');
        const toggleSwitch = document.querySelector("[data-theme-toggle]");
        console.log("Toggle switch checked:", toggleSwitch.checked);

        toggleSwitch.addEventListener("change", function() {
            // if checked, set dark mode
            
            if (toggleSwitch.checked) {
                document.querySelector("html").setAttribute("data-theme", "dark");
            }
            else{
                document.querySelector("html").setAttribute("data-theme", "light");
            }
        });
        
        [].forEach.call(links, function(link){
            link.addEventListener("click", navigate)
        });

        pages[currentIndex].classList.add("active");
        links[currentIndex].classList.add("active");  // Make sure the first link is active

    });

    function navigate(ev) {
        ev.preventDefault();

        const id = ev.currentTarget.href.split("#")[1];
        const newIndex = [...pages].findIndex(page => page.id === id);

        if (newIndex === currentIndex) return false; // Do nothing if the same page is clicked

        pages[currentIndex].classList.remove('active');
        links[currentIndex].classList.remove('active');

        pages[newIndex].classList.add('active');
        links[newIndex].classList.add('active');

        currentIndex = newIndex;

        return false;
    }


    return {
        pages,
        links,
        xhr: ajax
    }
})();
