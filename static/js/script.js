const searchInput = document.querySelector("#search-input")
const searchData = document.querySelector("#search-data")
searchInput.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;
    fetch('/search/', {
        method: 'POST',
        body: JSON.stringify({'search_text': searchValue})
    }).then(
        (res) => res.json()
    ).then(
        (data) => {
            console.log(data)
            searchData.innerHTML = ''
            if (data.length > 0) {
                data.forEach((item) => {
                    searchData.innerHTML += `
                        <h4>Продукт: ${item.title} </h4>
                        <p>Описание:${item.description} </p>
                        <p>Цена:${item.price} </p>
                        <hr>
                    `
                })
            }
        }
    )
})



function set_product_count() {
    const product_span = document.querySelector("#product-count-block")
    product_span.innerHTML = "(10)"
    fetch("/product/count/", {
        method: "GET"
    }).then(
        (res) => res.json()
    ).then(
        (data) => {
            product_span.innerHTML= `${data.count}`
        }
    )
}