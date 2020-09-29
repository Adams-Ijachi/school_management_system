$(document).ready(function(){
    $('.delete-row').click(function(e)
     { e.preventDefault()
       var btn_url = $(this).attr("data-url")
       var id = $(this).parents("tr").children("td:eq(0)").text()
       var name = $(this).parents("tr").children("td:eq(4)").text()
        $("#modal-delete").modal("show")
        $("#name").text(name)
        $("#user_id").val(id)

       $('#delete-user').click(function(e){
         e.preventDefault()
         $.ajax({
        
          url:btn_url,
          type:'POST',
          dataType:'Json',
          
         }).done(function(response){
           alert(response)
           $("#modal-delete").modal("hide")
           location.reload()
         })
         .fail(function(){
           alert('Not Deleted')
         })
         
           
       })

     })

    
  })