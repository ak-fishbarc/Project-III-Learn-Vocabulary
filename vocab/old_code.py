"""

{% extends 'base.html' %}

{% block content %}
    {% block javascript %}
    <script type="text/javascript">

        var data = null

        function get_cards(setname){

            response = fetch('http://127.0.0.1:5000/to_card')
            .then(response => response.json())
            .then(response => data = response[setname])

            }

        var counter = 0

        function get_card(){

           if (counter < data.length-1) {
               counter += 1
               }
           else{
               counter = 0
               }
           document.getElementById('card').innerHTML = data[counter]

        }
    </script>
    {% endblock %}
    {% for sets in wordsets %}
        {% if sets.name != None %}
            <div id='set' onclick="get_cards('{{ sets.name }}')">{{ sets.name }}</div>
        {% endif %}
    {% endfor %}

    <div style="background: grey; width: 100px; height: 150px; text-align: center; border-style: inset;" onclick="get_card()">
        <p id="card" style="position: relative; top: 25%; width: 100%;">Card</p></div>
{% endblock %}





@app.route('/memory', methods=['GET', 'POST'])
@login_required
def memory():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    wordsets = user.word_sets.all()
    return render_template('memory.html', wordsets=wordsets)


@app.route('/to_card', methods=['GET', 'POST'])
@login_required
def to_card():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    wordsets = user.word_sets.all()
    data = {}
    for sets in wordsets:
        if sets.words != None:
            data[sets.name] = sets.words.split(',')
    return data


"""