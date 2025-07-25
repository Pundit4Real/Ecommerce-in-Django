console.log("working fine");

const monthNames = ["Jan","Feb", "Mar", "April", "May", "June", "July", "Aug", 
"Sept", "Oct", "Nov","Dec"
];

$("#commentForm").submit(function(e){
    e.preventDefault();

let date = new Date();
let time = date.getDate() +  "  "  + monthNames[date.getMonth()] + ", " + date.getFullYear()

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function(resp){
            console.log("commeent saved to DB.....")


            if(resp.bool==true){
                $("#review-resp").html("Review added successfully.")
                $(".hide-comment-form").hide()
                $(".add-review").hide()

                // appending the form
                let _html =  '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html += '<div class="user justify-content-between d-flex">'
                    _html += '<div class="thumb text-center">'
                    _html += '<img src="https://www.shutterstock.com/image-vector/default-avatar-profile-icon-social-600nw-1677509740.jpg" alt="">'
                    _html += '<a href="#" class="font-heading text-brand">'+  resp.context.user +'</a>'
                    _html += '</div>'

                    _html += '<div class="desc">'
                    _html += '<div class="d-flex justify-content-between mb-10">'
                    _html += '<div class="d-flex align-items-center">'
                    _html += '<span class="font-xs text-muted">' + time + '</span>'
                    _html += '</div>'

                    for(let i = 1; i<=resp.context.rating; i++){
                        _html += '<i class= "fas fa-star text-warning"></i>';
                    }
                    
                    _html += '</div>'
                    _html += '<p class="mb-10">'+ resp.context.review +'</p>'

                    _html += '</div>'
                    _html += '</div>'
                    _html += '</div>'

                    $(".comment-list").prepend(_html); // Prepend the new review to the top of the list
                }

        }
    })

})


$(document).ready(function(){
    $(".filter-checkbox, #price-filter-btn").on("click", function(){
        console.log("checkbox have been clicked")

        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter") // vendor,category

            // console.log("filter value is:", filter_value);
            // console.log("filter key is:", filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key +']:checked')).map(function(element){
                return element.value
            })
        })

        console.log('filter object is: ', filter_object);

        $.ajax({
            url: '/filter-products',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log('Trying to send data....');
            },
            success: function(response){
                console.log(response);
                console.log('data sent');

                $("#filltered-product").html(response.data)
            }
        })
    })

    $("#max_price").on("blur",function(){
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()


        if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){

            min_price = Math.round(min_price * 100) / 100
            max_price = Math.round(max_price * 100) / 100

            alert("Price must be between $" +min_price +  ' and $' +max_price)
            $(this).val(min_price)
            $("#range").val(min_price)

            $(this).focus()
            return false
        }
    })



    // Add to cart functionality
    $(".add-to-cart-btn").on("click", function(){

        let this_val = $(this)
        let index = this_val.attr('data-index')

        let quantity = $(".product-quantity-" + index).val()
        let product_title = $(".product-title-" + index).val()

        let product_id = $(".product-id-" + index).val()
        let product_price = $(".current-product-price-" + index).text()

        let product_pid = $(".product-pid-" + index).val()
        let product_image = $(".product-image-" + index).val()

        console.log("qty:", quantity)
        console.log("title:", product_title)
        console.log("price:", product_price)
        console.log("id:", product_id)
        console.log("pid:", product_pid)
        console.log("image:", product_image)

        $.ajax({
            url: '/add-to-cart',
            data:{
                'id': product_id,
                'pid': product_pid,
                'image':product_image,
                'qty': quantity,
                'title': product_title,
                'price': product_price,

            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Adding product to cart.....")
            },
            success: function(response){
                this_val.html("✔")
                console.log("Added product to cart");
                $(".cart-items-count").text(response.totalcartitems)
            }
        })
    })

    $(".delete-product").on("click", function(){

        let product_id = $(this).attr("data-product")
        let this_val = $(this)

        console.log("Product Id:", product_id);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend:function(){
                this_val.hide()
            },
            success:function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    })


    // updating cart
    $(".update-product").on("click", function(){

        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let Product_quantity = $(".product-qty-"+product_id).val()

        console.log("Product Id:", product_id);
        console.log("Product QTY:", Product_quantity);


        $.ajax({
            url: "/update-cart",
            data: {
                "id": product_id,
                "qty":Product_quantity
            },
            dataType: "json",
            beforeSend:function(){
                this_val.hide()
            },
            success:function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    })

    // Making Default Addresses
    $(document).on("click", ".make-default-address", function() {
        let id = $(this).attr("data-address-id")
        let this_val = $(this)

        console.log("id", id);
        console.log("element:", this_val);

        $.ajax({
            url: "/make-default-address",
            data: {
                "id":id
            },
            dataType:"json",
            success: function(response){
                console.log("address made default")
                if(response.boolean == true){
                    $(".check").hide()
                    $(".action_btn").show()

                    $(".check"+id).show()
                    $(".button"+id).hide()
                }
            }
         })
    })

    //Adding to Wishlist
    $(document).on("click",".add-to-wishlist", function(){
        let product_id = $(this).attr("data-product-item")
        let this_val = $(this)

        console.log("product id", product_id);

        $.ajax({
            url: "/add-to-wishlist",
            data: {
                "id":product_id
            },
            dataType:"json",
            beforeSend: function(){
                console.log("Adding to wishlist")
            },
            success: function(response){
                this_val.html("✔")
                if (response.bool == true){
                    console.log("added to wishlist");
                }
            }
        })
    })

    //Remove from wishlist
    $(document).on("click",".delete-wishlist-product",function(){
        let wishlist_id = $(this).attr("data-wishlist-product")
        let this_val = $(this)

        console.log("wishlist id", wishlist_id)

        $.ajax({
            url: "/remove-from-wishlist",
            data: {
                "id": wishlist_id
            },
            dataType:"json",
            beforeSend: function(){
                console.log("Deleting product from wishlist...");
            },
            success: function(response){
                $("#wishlist-list").html(response.data)

            }
        })
    })

    $(document).on("submit","#contact-form-ajax", function(e){
        e.preventDefault()
        console.log("Submited..",);

        let full_name = $("#full-name").val()
        let email = $("#email").val()
        let phone = $("#phone").val()
        let subject = $("#subject").val()
        let message = $("#message").val()

        console.log("Name:",full_name)
        console.log("Email:",email)
        console.log("Phone:",phone)
        console.log("subject:",subject)
        console.log("Message:",message)


        $.ajax({
            url: "/ajax-contact-form",
            data: {
                "full_name":full_name,
                "email":email,
                "phone":phone,
                "subject":subject,
                "message":message,
            },
            dataType:"json",
            beforeSend: function(){
                console.log("Sending data to server")
            },
            success: function(response){
                console.log("Sent data to server")
                $(".message-response").hide()
                $("#contact-form-ajax").hide()
                $("#message-response").html("Message sent successfully.")


            }
        })

    })
})
