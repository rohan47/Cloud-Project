# Cloud-Project
I am working my own cloud project and named it Hooper. It is a basic cloud having the following services :

1. Software as a service (SAAS) 
2. Storage as a service(STAAS). It has again two type of services :
   - Object Storage     
   - Block Storage 
3. Infrastructure as a service (IAAS) 
4. Container as a service (CAAS) 
5. Platform as a service (PAAS) 

### Background technologies used :
1. For SAAS i used X11 Forwarding property of SSH protocol to provide software to clients. 
2. Storage :
   - For object storage i have used Glusterfs.     
   - For block storage i have used iSCSI protocol. 
3. For infrastructure as a service i used qemu-kvm for providing virtualized cloud OS to the client and to provide it on browser i used noVNC.
4. For container as a service i used Dockers and to provide it to clients browser i used shellinabox tool. 
5. Again for PAAS i used Dockers.

### For Web Application :
  - Back-end:- Python CGI 
  - Front-end:- HTML and CSS Database:- MongoDB
