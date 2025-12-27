
const list = document.getElementById("products-list");


const formatPrice = (price) =>{
    return Number(price).toLocaleString("fa-IR");
};


const showProduct = (item) => {
    const div = document.createElement("div");
    div.className = "product";
    
    // Create link
    const link = document.createElement("a");
    link.href = DETAIL_URL_TEMPLATE.replace("PRODUCT_ID", item.id);
    link.style.textDecoration = 'none';
    link.style.color = 'inherit';
    link.style.display = 'block';
    
    
 
    if (item.images && item.images.length > 0) {
        const image = document.createElement("img");
        image.src = item.images[0].image_url;
        image.alt = item.name;
        image.className = "image";
        link.appendChild(image);  // ← Add to LINK
    }
    

    const title = document.createElement("h3");
    title.textContent = item.name;
    title.className = "product-title";
    link.appendChild(title);  // ← Add to LINK
    
    
    const price = document.createElement("p");
    price.textContent = `${item.price.toLocaleString('fa-IR')} تومان`;
    price.className = "product-price";
    link.appendChild(price);  // ← Add to LINK
    
    div.appendChild(link);
    
    
    return div;
};



async function getProducts () {
    const res = await fetch("/api/products");
    const data = await res.json();
    const products = data.results || data;
    products.forEach(product =>{
        list.appendChild(showProduct(product));
    });
};

document.addEventListener("DOMContentLoaded", getProducts);




// fetch("/api/products")
// .then(res => res.json())
// .then(data => {
//         const products = data.results || data;
//         products.forEach(item => {
//             list.appendChild(showProduct(item));
//         });
// })

    
