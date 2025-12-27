const loadProductDetails = async()=>{
    try{
         console.log(API_URL);
         const response = await fetch(API_URL);
         if(!response.ok){
             throw new Error('محصول یافت نشد');
         }
         const product = await response.json();
         console.log(product);
         displayProduct(product);
    }

    catch(error){
        console.error('Error:', error);
    }
  
};

const displayProduct = (product) =>{
    const container = document.getElementById('product-detail-page');
    
    const detailDiv = document.createElement('div');
    detailDiv.className = "product-detail-content";

    const galleryDiv = document.createElement('div');
    galleryDiv.className = "image-gallery"

    if(product.images && product.images.length>0){
        const mainImage = document.createElement('img');
        mainImage.src = product.images[0].image_url;
        mainImage.className = 'main-image';
        mainImage.id = 'main-image';
        mainImage.alt = product.name;
        galleryDiv.appendChild(mainImage);
    }
        if(product.images && product.images.length>1){
            const thumbDiv = document.createElement('div');
            thumbDiv.className = 'thumbnails';
            
            product.images.forEach((img, index)=>{
                const thumb = document.createElement('img');
                thumb.src = img.image_url;
                thumb.className = 'thumbnail'; 
                thumb.onclick = ()=>{
                    document.getElementById('main-image').src = img.image_url;
                }
                thumbDiv.appendChild(thumb);             
            });
            galleryDiv.appendChild(thumbDiv);
    }
    



    detailDiv.appendChild(galleryDiv);

    const infoDiv = document.createElement('div');
    infoDiv.className = "product-info";
    infoDiv.innerHTML = `
    <h1>${product.name}</h1>
    <p class="price">${product.price.toLocaleString('fa-IR')} تومان </p>
    <p class="size">${product.size}</p>
    <p class="description">${product.description}</p>
    <button class="add-to-cart"> افزودن به سبد خرید</button>
    `

    detailDiv.appendChild(infoDiv);
    container.appendChild(detailDiv);
}


document.addEventListener("DOMContentLoaded", loadProductDetails);




