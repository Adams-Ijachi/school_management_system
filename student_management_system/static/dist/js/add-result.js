
    $(document).ready(function(){
 
        $('#fetch_student').click(function(){
          var grade =$('#subject').val();
            
            var session =$('#session').val();


              $.ajax({
                 url:'/add_result_list',
                 type:'POST',
                 data:{subject:grade,session:session},
                 method:'POST',
              })
              .done(function(response){

                  var json_data = response;
                  var div_data ='<thead><tr> <th> Student Attendance </th> <th> Status </th> </tr></thead>';
                  if(json_data.length>0){
                      for( key in json_data )
                      {
                        //  div_data +="<option value='"+json_data[key][0] +"'>"+json_data[key][1]+"</option>";
                         div_data +="<tr><td><input type='hidden' checked='checked'  name='student_data[]'  value='"+json_data[key][0] +"'><label class='form-check-label' style='padding:10px' > <b>"+json_data[key][1]+" </b></label> </td><td> <button type='button' class='btn btn-success score_btn' value='"+json_data[key][0] +"' >Add Score</button></td></tr>";
                      }
                      

                     
                      $('#students').html(div_data);
                      $('.score_btn').click(function(e){
                        e.preventDefault()
                        var id = $(this).attr("value")
                        var name = $(this).parents("tr").children("td:eq(0)").text()
                      
                        $("#student_name").text(name)
                        $("#student_id").val(id)

                        $("#subject_value").val(grade)
                        $("#session_value").val(session)
                        
                        $("#modal-result").modal("show")


                          
                        
                         })

                      }
                      else{

                         $('#error_attendance').html('No Students Found');
                          $('#error_attendance').show();


                      }


                  })
              .fail(function(){
              alert('Error')
              });
           

        });
        $('#save_result').click(function(e){
                e.preventDefault()
                var subject =$('#subject_value').val();
                var session =$('#session_value').val();
                var student_id =$('#student_id').val();
                var first_test=$('#first_test').val();
                var second_test=$('#second_test').val();
              $.ajax({
                 url:'/save_result',
                 type:'POST',
                 data:{session:session,student_id:student_id,subject:subject,first_test:first_test,second_test:second_test}

              })
               .done(function(response){
                 alert(response)
                 location.reload()
                 
               }).fail(function(){
                 alert('not added')
               })
               


            })
       
    
   
    });
