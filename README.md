# Deletable Branch Finder

## Introduction

All the branches in the organisation you have access to will be searched for 
branches you have authored but not closed.  
As it runs it will print out the repo names in the following format:  
`<repo-index>/<total-repos> - <repo-name>`  

If a branch of yours is found and is not deleted it will print:  
```
135/192 - <repo-name>
	DELETE: <branch-name>
```  

If the author of the branch is returned as null it will print as such:  
```
139/192 - <repo-name>
	<branch-name>
		 + Author null
		 | Committer name: <committer-name>
		 - Possibly yours: <boolean> 
```

This won't match unfortunately, however, it will tell you if it's probably yours based on the name.


## Installation

1. Make a virtualenv  
`virtualenv virtualenv`

2. Activate the virtualenv  
`. virtualenv/bin/activate`

2. `pip install requests`

2. `python branch-finder.py <username> <organisation>`

3. Enter password when prompted
