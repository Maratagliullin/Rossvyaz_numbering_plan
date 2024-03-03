function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

var app = new Vue({
  el: '#app',

  data: {
    errors: [],
    phone_number:null,
    info: [],
    number:null,
  },
  methods: {
    submit: function (event) {
       axios.post('/api/v1/info', {
       number: this.phone_number,
      },{
    headers: {
        'X-CSRFToken': csrftoken
    }
})
      .then(response => {
           this.info = [];
           this.errors = [];
           for (var i = 0; i < response.data.number.length; i++) {
                if (typeof(response.data.number[i]) === "object") {
                      this.info.push({
                      number: response.data.number[i].number,
                      operator: response.data.number[i].operator.replace(/"/g,""),
                      region: response.data.number[i].region.replace(/"/g,"")
                      })
                }
                 else{
                    this.errors.push({
                     error_text: response.data.number[i]
                     });
                }
           }
      })
      .catch(error => {
      });
      event.preventDefault();
      }
  }
})

