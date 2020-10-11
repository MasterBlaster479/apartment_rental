<template>
  <div id="form">
    <h1>Calendar events</h1>
    <b-form inline @submit="import_calendars">
        <br />
        <b-form-group
                id="input-group-1"
                label="Date from:"
                label-for="input-1"
        >
            <b-form-input
            id="input-1"
            v-model="date_from"
            type="date"></b-form-input>
        </b-form-group>
        <b-form-group
                id="input-group-2"
                label="Date to:"
                label-for="input-2"
                >
            <b-form-input
            id="input-2"
            v-model="date_to"
            type="date"></b-form-input>
        </b-form-group>
         <b-button type="button" variant="primary" v-on:click="get_calendars">Fetch</b-button>

         <b-form-file
          v-model="file"
          :state="Boolean(file)"
          placeholder="Choose a file or drop it here..."
          drop-placeholder="Drop file here..."
          id="file1" required
        ></b-form-file>
        <div class="mt-3">Selected file: {{ file ? file.name : '' }}</div><br />
        <b-button type="submit" variant="secondary">Import</b-button>
    </b-form>
    <b-table hover :items="calendars"></b-table>
  </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: 'calendar',
        data() {
            return {
                date_from: null,
                date_to: null,
                calendars: [],
                files: [],
                file: null
            }
        },
        methods: {
            handleFilesUpload() {
                let uploadedFiles = this.$refs.files.files;
                /*
                  Adds the uploaded file to the files array
                */
                for( var i = 0; i < uploadedFiles.length; i++ ){
                  this.files.push( uploadedFiles[i] );
                }
                this.files = uploadedFiles;
                console.log(this.files);
            },
             get_calendars: function() {
                axios.get('/calendars', {params:{date_from: this.date_from, date_to: this.date_to}})
                .then(response => {this.calendars = response.data})
                .catch(function(error){
                    console.log(error)
                })
            },
            import_calendars: function(event) {
                event.preventDefault();
                let formData = new FormData();
                formData.append('file', this.file)
                console.log(formData.get('file'))
                axios.post('/import-calendar', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        },
                    }
                    )
                .then(response => {this.get_calendars()})
                .catch(function(error){
                    console.log(error)
                })
            }
        }
    }
</script>

<style>
    #form{
        position: absolute;
        left: 35%;
    }
    #input-group-1{
        width:250px;
    }
    #input-group-2{
        width:250px;
    }
    #file1{
        width: 200px;
    }
</style>