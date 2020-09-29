$(document).ready(function(){
    $('#fetch_student_edit').click(function(){
      fetchStudent();
     });
     $('#save_result').click(function(){
       SaveEditedResult();
     });
     $('#delete-result').click(function(e){
       e.preventDefault()
       var url = $(this).attr('data-url')
       
       DeleteResult(url);
     })
    
   
     function fetchStudent(e){
            
            var session =$('#id_session_id').val();
            var grade =$('#id_subject_id').val();
          
            $.ajax({

            url:'/add_result_list',
            type:'POST',
            data:{subject:grade,session:session},
            })
            .done(function(response){

                var json_data = response;
                var div_data ='<thead><tr> <th> Student Attendance </th> <th> Action </th> <th> Delete </th> </tr></thead>';
                if(json_data.length>0){
                  for( key in json_data )
                  {

                    div_data +="<tr><td><input type='hidden' checked='checked'  name='student_data[]'  value='"+json_data[key][0] +"'><label class='form-check-label' style='padding:10px' > <b>"+json_data[key][1]+" </b></label> </td><td> <button type='button' class='btn btn-success  score_btn'  id='id_student_id' value='"+json_data[key][0]+"' >Edit Result</button></td><td><button type='button' class='btn btn-danger  delete_result_btn' value='"+json_data[key][0] +"' >Delete</button></td></tr>";

                    }
                      $('#students').html(div_data);
                     
                  }
                else{

                       $('#error_attendance').html('No Students Found');
                        $('#error_attendance').show();
                        
                        $(function(){
                            var duration = 5000;
                            setTimeout(function (){
                                 $('#error_attendance').hide();}, duration);
                            })
                    }
                    $('.score_btn').click(function(){
                      var id = $(this).attr("value")
                      var subject_id = $('#id_subject_id').val();
                      var session =$('#id_session_id').val();
                     fetchStudentModal(id,subject_id,session)
                    });
                    //DELETE RESULT
                  $('.delete_result_btn').click(function(){
                      var id = $(this).attr("value")
                      var subject_id = $('#id_subject_id').val();
                      var session =$('#id_session_id').val();
                      $("#modal-result-delete").modal("show")
                      var names = $(this).parents("tr").children("td:eq(0)").text()
                      $("#name_delete").text(names)
                      $("#student_id_delete").val(id)
                      $("#subject_value_delete").val(subject_id)
                      $("#session_value_delete").val(session)
                      
                    
                  })

             })
            .fail(function(){
            alert('Error')
            });
          };
      function fetchStudentModal(id,subject_id,session){
        $("#modal-result-edit").modal("show")
            
            var student_id = id
            var subject_id = subject_id
            var session = session
            
            
            $.ajax({

               url:'/staff_student_result',
                type:'POST',
                data:{student_id:student_id,subject_id:subject_id,session:session},
                 })
                 .done(function(response){

                   if(response == 'False'){
                    $('#first_test').val('');
                    $('#second_test').val('');
                     alert('Result Not Found')
                     
                     $('#save_result').attr('disabled',true)
                     $('#save_result').text('Cant edit cause no result')
                   }
                   else{
                     
                       var json_data = response;
                       console.log(response)
                       $('#save_result').attr('disabled',false)
                       $('#first_test').val(json_data['first_test']);
                       $('#second_test').val(json_data['second_test']);
                       $('#result_id').val(json_data['id']);
                       $('#save_result').text('Save')
                       $("#student_id").val(student_id)
                       $("#subject_value").val(subject_id)
                       $("#session_value").val(session)
                     }

                   })
            
      };
      function SaveEditedResult(e){
        
        var first_test=$('#first_test').val();
        var second_test=$('#second_test').val();
        var subject_id =$('#subject_value').val();
        var session_id =$('#session_value').val();
        var student_id =$('#student_id').val();
         
        $.ajax({

          url:'/staff_edit_result',
          type:'POST',
          data:{student_id:student_id,subject_id:subject_id,session_id:session_id,first_test:first_test,second_test:second_test },
            })
            .done(function(response){
              if(response === 'True'){
                
                location.reload()
                $(function(){
                    var duration = 5000;
                    setTimeout(function (){
                          $('#success-alert').hide();}, duration);
                    })
              }
              if(response === 'False'){
                location.reload()
                
              }
            })

        };
          function DeleteResult(url){
            var subject_id =$('#subject_value_delete').val();
            var session_id =$('#session_value_delete').val();
            var student_id =$('#student_id_delete').val();

            $.ajax({
              url:url,
              type:'POST',
              data:{subject_id:subject_id,session_id:session_id,student_id:student_id}
           })
           .done(function(response){
             alert(response)
             location.reload()
           })
           .fail(function(){
             alert('error')
             location.reload()
           })

           
           
          };
    
             



  });