odoo.define('partner_files.custom_script', function(require) {
    'use strict';

    var FormController = require('web.FormController');
    

    var CustomFormController = FormController.include({
        events: _.extend({}, FormController.prototype.events, {
            'change .o_folder_selector': '_onFolderChange',
        }),

        init: function(parent, model, renderer, params) {
            this._super.apply(this, arguments);
            // Additional initialization if necessary
        },

        _onFolderChange: function(event) {
            var folderId = $(event.currentTarget).val();
            this._filterFilesByFolder(folderId);
        },

        _filterFilesByFolder: function(folderId) {
             // Get all records (files) from One2Many field
            var allFiles = this.value.data;

            // Filter logs based on folder ID
            var filteredFiles;
            if (folderId) {
                filteredFiles = allFiles.filter(function(file) {
                    return file.data.folder_id && file.data.folder_id.data.id === folderId;
                });
            } else {
                // If no folder is selected, show all files
                filteredFiles = allFiles;
            }

            // Update view with leaked files
            this.renderFiles(filteredFiles);
        },

        renderFiles: function(files) {
            // Logic to update the display of files in the user interface
            var $fileListContainer = this.$('.file-list-container');
            $fileListContainer.empty(); // Limpiar la lista actual
        
            files.forEach(function(file) {
                var $fileEntry = $('<div/>', { 'class': 'file-entry', 'text': file.data.name });
                $fileListContainer.append($fileEntry);
            });
        }
     });

    return CustomFormController;
});

odoo.define('partner_files.FileListWidget', function(require) {
    'use strict';

    var FieldOne2Many = require('web.relational_fields').FieldOne2Many;
    var registry = require('web.field_registry');

    var FileListWidget = FieldOne2Many.extend({
        events: _.extend({}, FieldOne2Many.prototype.events, {
            'keyup .o_search_input': '_onSearchInput',
        }),

        _onSearchInput: function(event) {
            var searchValue = event.target.value.toLowerCase();
            this._filterFilesByName(searchValue);
        },

        _filterFilesByName: function(searchValue) {
            // Logic to filter files by name
            var allFiles = this.value.data;

            var filteredFiles = allFiles.filter(function(file) {
                return file.data.name.toLowerCase().includes(searchValue);
            });

            this._renderFiles(filteredFiles);

        },

        _renderFiles: function(files) {
            // Logic to render the files
            var $fileListContainer = this.$('.file-list-container');
            $fileListContainer.empty(); // Clear current list
            files.forEach(function(file) {
                var $fileEntry = $('<div/>', { 'class': 'file-entry', 'text': file.data.name });
                // Add more details or actions for each file if necessary
                $fileListContainer.append($fileEntry);
            });
        },
    });

    registry.add('my_file_list_widget', FileListWidget);

    return FileListWidget;
});