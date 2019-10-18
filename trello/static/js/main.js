$(document).ready(function () {

    $('#board-modal').on('shown.bs.modal', function(event) {
       var remoteUrl =  $(event.relatedTarget).data('remote') 
       var modal = $(this)
       $.ajax({
            method: 'GET',
            url: remoteUrl
       }).done(function(response){
        modal.find('.modal-body').html(response)
       })
      })

      $(document).on('submit','#board_new_form', function(event){
         event.preventDefault()
         var action = $(this).attr('action')
         var board_data = $(this).serialize()
         
         $.ajax({
            method: 'POST',
            url: action,
            data: board_data
         }).done(function(response){
            window.location.href =''             
         }).fail(function(response){
            var error_template = '<br><ul><li>This Field is required</li></ul>';
            $('.error-add-board').html(error_template)
         })
      })

      




      $('#board-edit-modal').on('shown.bs.modal', function(event) {
         var remoteUrl =  $(event.relatedTarget).data('remote') 
         
         var modal = $(this)
         $.ajax({
              method: 'GET',
              url: remoteUrl
         }).done(function(response){
          modal.find('.modal-body').html(response)
         

         })
        })


        $(document).on('submit','#board_edit_form', function(event){
         event.preventDefault()
         var action = $(this).attr('action')
         var board_data = $(this).serialize()
         $.ajax({
            method: 'POST',
            url: action,
            data: board_data
         }).done(function(response){
            window.location.href ='' 
         }).fail(function(response){
            var error_template = '<br><ul><li>This Field is required</li></ul>';
            $('.error-edit-board').html(error_template)
         })
      })



      $('#list-add-modal').on('show.bs.modal', function(event){
         var remoteUrl = $(event.relatedTarget).data('remote')
         var modal = $(this)
         
         $.ajax({
            method: 'GET',
            url: remoteUrl

         }).done(function(response){
            modal.find('.modal-body').html(response)
            
         })
      })

      $(document).on('submit','#list-add-modal', function(event){
         event.preventDefault()
         var action = $('#add_list_form').attr('action')
         var list_add_data = $('#add_list_form').serialize()
         var csrf = $('input[name="csrfmiddlewaretoken"]').val();
         $.ajax({
            method: 'POST',
            url: action,
            data: list_add_data,
            headers:{
               'X-CSRFToken':csrf
           }
         }).done(function(response){
            window.location.href ='' 
         }).fail(function(response){
            var error_template = '<ul><li>This Field is required</li></ul>';
            $('.error-add-list').html(error_template)
         })
      })




      



      $('#list-edit-modal').on('show.bs.modal', function(event){
         var remoteUrl = $(event.relatedTarget).data('remote')
         var modal = $(this)
         
         $.ajax({
            method: 'GET',
            url: remoteUrl

         }).done(function(response){
            
            modal.find('.modal-body').html(response)
         })
      })
      
      
      $(document).on('submit','#list-edit-modal', function(event){
         event.preventDefault()
         var action = $('#edit-list-form').attr('action')
         var list_edit_data = $('#edit-list-form').serialize()
         var csrf = $('input[name="csrfmiddlewaretoken"]').val();
         $.ajax({
            method: 'POST',
            url: action,
            data: list_edit_data,
            headers:{
               'X-CSRFToken':csrf
           }
         }).done(function(response){
            window.location.href ='' 
         }).fail(function(response){
            var error_template = '<ul><li>This Field is required</li></ul>';
            $('.error-edit-list').html(error_template)
         })
      })




      $('#card-add-modal').on('show.bs.modal', function(event){
         var remoteUrl = $(event.relatedTarget).data('remote')
         var modal = $(this)
         
         $.ajax({
            method: 'GET',
            url: remoteUrl

         }).done(function(response){
            
            modal.find('.modal-body').html(response)
         })
      })

      $(document).on('submit','#card-add-modal', function(event){
         var action = $('#add_card_form').attr('action')
         var add_card_data = $('#add_card_form').serialize()
         var csrf = $('input[name="csrfmiddlewaretoken"]').val()
         event.preventDefault()
         $.ajax({
            method: 'POST',
            url: action,
            data: add_card_data,
            headers:{
               'X-CSRFToken':csrf
           }
         }).done(function(response){
            window.location.href ='' 
         }).fail(function(response){
            var error_template = '<ul><li>This Field is required</li></ul>';
            $('.error-add-card').html(error_template)
         })
      })





      $('#card-edit-modal').on('show.bs.modal', function(event){
         var remoteUrl = $(event.relatedTarget).data('remote');
         var modal = $(this);
         $.ajax({
            method: 'GET',
            url: remoteUrl

         }).done(function(response){
            modal.find('.modal-body').html(response);
            
         })
      })

      $(document).on('submit','#card-edit-modal', function(event){
         
         var action = $('#edit_card_form').attr('action');
         var add_card_data = $('#edit_card_form').serialize();
         var csrf = $('input[name="csrfmiddlewaretoken"]').val();
         console.log(csrf)
         event.preventDefault()
         $.ajax({
            method: 'POST',
            url: action,
            data: add_card_data,
            headers:{
               'X-CSRFToken':csrf
           }
         }).done(function(response){

            window.location.href = '';
            
         }).fail(function(response){
            var error_template = '<ul><li>This Field is required</li></ul>';
            $('.error-edit-card').html(error_template)
         })
      })


      


 
     $('#archived-cards-modal').on('show.bs.modal', function(event){
      var remoteUrl = $(event.relatedTarget).data('remote')
      var modal = $(this)
      
      $.ajax({
         method: 'GET',
         url: remoteUrl

      }).done(function(response){
         
         modal.find('.modal-body').html(response)
      })
   })


   $('#invite-member-modal').on('show.bs.modal', function(event){
      var remoteUrl = $(event.relatedTarget).data('remote')
      var modal = $(this)
      
      $.ajax({
         method: 'GET',
         url: remoteUrl

      }).done(function(response){
         
         modal.find('.modal-body').html(response)
      })
   })


   $(document).on('submit','#invite-member-modal', function(event){    
      var action = $('#invite-member-form').attr('action');
      var add_card_data = $('#invite-member-form').serialize();
      var csrf = $('input[name="csrfmiddlewaretoken"]').val();
      event.preventDefault()
      $.ajax({
         method: 'POST',
         url: action,
         data: add_card_data,
         headers:{
            'X-CSRFToken':csrf
        }
      }).done(function(response){
         
         window.location.href = '';
         
      }).fail(function(response){
         var error_template = '<ul><li>This Field is required</li></ul>';
         $('.error-edit-card').html(error_template)
      })
   })


   $('#view-card-modal').on('show.bs.modal', function(event){
      
      var remoteUrl = $(event.relatedTarget).data('remote');
      var modal = $(this);
      $('#progress').hide();
      console.log(modal)
      $.ajax({
         method: 'GET',
         url: remoteUrl

      }).done(function(response){
         
         modal.find('.modal-body').html(response)
      })
   })

   $(document).on('submit','#card_attatchment_form', function(event){
      var action = $('#card_attatchment_form').attr('action');
      var csrf = $('input[name="csrfmiddlewaretoken"]').val();
      var data = new FormData($('#card_attatchment_form').get(0));
      event.preventDefault()
      $.ajax({
         method: 'POST',
         url: action,
         data: data,
         enctype: 'multipart/form-data',
         processData: false,
         contentType: false,
         headers:{
            'X-CSRFToken':csrf
         }
      }).done(function(response){   
         window.location.href = '';     
      }).fail(function(response){
         var error_template = '<ul><li>This Field is required</li></ul>';
         $('.error-add-attchment').html(error_template)
      })
   })

$(document).on('submit','#add_cl_form', function(event){    
      var action = $('#add_cl_form').attr('action');
      var add_card_data = $('#add_cl_form').serialize();
      var csrf = $('input[name="csrfmiddlewaretoken"]').val();
      
      event.preventDefault()
      $.ajax({
         method: 'POST',
         url: action,
         data: add_card_data,
         headers:{
            'X-CSRFToken':csrf
        }
      }).done(function(response){
         
         $('#view-card-modal').trigger("show")
         
      }).fail(function(response){
         var error_template = '<ul><li>This Field is required</li></ul>';
         $('.error-add-cl').html(error_template)
      })
   })


   $(".sort").sortable({
      connectWith: ".sort",
      over: function(event,ui){
         var card_list_id = $(this).data('id')
         var csrf = $('[name="csrfmiddlewaretoken"]').val()         
         var action = $(event.toElement).data('action')
         console.log(action)

         $.ajax({
            method: 'POST',
            url: action,
            data: {'id':card_list_id},
            headers:{
               'X-CSRFToken':csrf
           }
         }).done(function(response){

         })
      }
   })

   $(document).on('click','input', function() {
      
      var total = $('input[type="checkbox"]').length;
      var checked = $('input[type="checkbox"]:checked').length;
      var percentage = (checked/total)*100
      
      $('#progress-bar').css('width', percentage + '%').attr('aria-valuenow', percentage);
  });






});