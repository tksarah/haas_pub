# Hands-on as a Service

## Decryption
It is a private playbook.
 
## Requirement 

* ansible 2.3.0 
* docker 1.11.2
* dopy 0.3.5 (0.3.7 is broken , at 2017/1/14)

## Preparation

**Edit : roles/apache/vars/main.yml**

This is http://＜ server address ＞/＜ web_alias ＞/ .

```
web_alias: "haas"
```

## Options Variables

**roles/handson/vars/main.yml**

```
download: true             # If you want to download after this play finised , it's true. (default: false) 
digest: false              # When you use Digest Authorication , it's true. (default: false)
```


## For OpenStack (Test)
```
ansible-playbook -i hosts -e "target=ops-home vtype=OpenStack hname=hoge" site.yml
```

## For DigitalOcean (Cloud)

```
ansible-playbook -i hosts -e "target=dc vtype=DC hname=hoge" site.yml
```
