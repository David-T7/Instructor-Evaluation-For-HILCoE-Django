(function($){
    $(document).ready(function(){
        $('#id_criteria_descriptions').after('<button type="button" id="add-criteria">+</button>');
        
        $('#add-criteria').click(function() {
            var criteriaInput = $('<input type="text" name="criteria_descriptions" class="vTextField">');
            criteriaInput.insertBefore('#add-criteria');
        });
    });
})(django.jQuery);
