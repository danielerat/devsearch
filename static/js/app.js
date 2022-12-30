let alertWrapper = document.querySelector('.alert')
let alertClose = document.querySelector('.alert__close')
if (alertWrapper) {

    alertClose.addEventListener('click', () => alertWrapper.style.display = 'none')
}
// Get Search form and page links
let searchForm = document.querySelector('#searchForm')
let pageLinks = document.querySelectorAll('.page-link')

//Makes sure the search form exists
if (searchForm) {
    console.log("yea we are there")
    for (let i = 0; pageLinks.length > i; i++) {
        pageLinks[i].addEventListener('click', function (e) {
            e.preventDefault()
            console.log(pageLinks[i])
            //Get the data attribute data-page
            let page = this.dataset.page
            // Add hidden input to search form
            searchForm.innerHTML += `<input value=${page} name='page' hidden />`
            //Submit Form now
            searchForm.submit()

        })
    }
}
