<h1>Nmap project panel</h1>
<p>Python script managing nmap results in projects.<br>
I created it to practice the Flask framework for a school assignment.</p>

<h2>Functionality</h2>
<p>The focus of the script is managing results of nmap scans. You can create projects that are linked to user accounts.
The results get saved to a SQLite database using Flask SQLAlchemy. The results get rendered to the user in a html table that is sortable on every
column.
</br>
The projects are shareble between multiple users. 

<h2>Installation</h2>
<p>It is recommended to install the python dependencies in a separate virtual environment.
In the root folder, there is a requierements.txt file. Use this to install the dependencies:
<code>pip3 install -r requirements.txt</code></p>
<p>To start the script, just run the app.py file: <code>python3 app.py</code></p>

<h2>Future development</h2>
<p> - More Nmap settings (sC, O, etc.)<br>
    - A discovery panel to scan an IP range for online devices <br>
    - Threaded scanning.</p>


