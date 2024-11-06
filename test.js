var sub_total = 0.0;



 
$(".input-spinner").click(function(){
  var b =parseFloat($(this).parent().find("input").val())
//   console.log(b)
  var price =$(this).parents().siblings(".price-col").text()
 var c = parseFloat(price.replace("$",""));
//  	console.log(c);
// console.log(price)
  var total_amt = c*b;
//   console.log(total_amt)
  $(this).parents().siblings(".total-col").html("$"+total_amt)
  
 
});

$(".input-group-prepend").click(function(){
  console.log("click")
  var a = parseInt ($(this).parent().siblings().val())
  if (a<=1 || a>=10){
    console.log("calling sum",z=(calculating_total_sum()))
   alert("you cant add product")
  }
  else{
  sub_total -= calculating_total_sum()
  }
  console.log("total amt is :" , sub_total)
  
})

$(".input-group-append").click(function(){
  console.log("click")
  var a = parseInt ($(this).parent().siblings().val())
  console.log(a)
  if (a<=1 || a<=10){
    
  sub_total += calculating_total_sum()
  }
  else{
  alert("limit !!!")
     
  }
  
  console.log("total amt is :" , sub_total)
  
})


function calculating_total_sum(){
   $(".total-col").each(function(){
            var a =parseFloat($(this).text().replace("$",""))
          //   console.log(a)
             return a
          
            
          })
}

