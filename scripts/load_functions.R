#Functions----
calculate_LCA<-function(host2virus){
  host2virus<-data.frame(host2virus)
  colnames(host2virus)<-c("Virus","Kingdom","Phylum","Class","Order","Family","Genus","Species")
  host2virus$Species<-gsub(" NA","",host2virus$Species)
  viruscount<-host2virus$Virus %>% table%>% data.frame()
  one<-subset(viruscount,Freq==1)[,1]
  more<-subset(viruscount,Freq>1)[,1]
  sub1<-subset(host2virus,Virus %in% one & Species!="s__")[,c("Species","Virus")]
  sub2list<-subset(host2virus,Virus %in% one & Species=="s__")[,"Virus"]
  sub2<-subset(host2virus,Virus %in% sub2list)[,c("Species","Virus")]
  # sub2$Host<-gsub("s__ NA","s__",sub2$Host)
  names(sub2)<-names(sub1)
  subone<-rbind(sub1,sub2)
  if(!length(subone$Species)==0){
    subone$"level"<-"Species"
    names(subone)<-c("LCA","Virus","level")
  }
  submore<- data.frame(LCA="LCA",Virus="Virus",level="level")
  for(i in more){
    link<-subset(host2virus,Virus==i)
    for(k in 2:8){
      num<-unique(link[,k]) %>% length
      if(num>1 & k==2){
        level="Kingdom"
        name<-""
        break
      }
      if(num>1){
        level=switch(k-2,"Kingdom","Phylum","Class","Order","Family","Genus","Species")
        name<-unique(link[,k-1])
        if(unique(link[,k])=="s__"){
          level=switch(k-2,"Kingdom","Phylum","Class","Order","Family","Genus","Species")
          name=unique(link[,k-1])
        }
        break
      }
      #print(i)
      if(num==1 & k==8){
        level="Species"
        name<-unique(link[,k])
        if(unique(link[,k])=="s__"){
          level="Genus"
          name=unique(link[,k-1])
        }
        break
      }
    }
    lca<-c(name,i,level)
    submore<-rbind(submore,lca)
  }
  #names(submore)<-c("LCA","Virus","level")
  submore<-submore[-1,]
  all<-rbind(subone,submore)
  return(all)
}
get_UP_degenerate_bases<-function(s){
  #   # ss<-replace(s,pattern=c("N:N","D:[DN]",
  #   #                         "V:[VN]","B:[BN]",
  #   #                         "H:[HN]","W:[WHDN]",
  #   #                         "S:[SBVN]","K:[KBDN]",
  #   #                         "M:[MHVN]","Y:[YHBN]",
  #   #                         "R:[RVDN]","C:[CYMSHBVN]",
  #   #                         "G:[GRKSBVDN]","T:[TYKWHBDN]","A:[ARMWHVDN]"))
  ss<-gsub("D","[DN]",s)
  ss<-gsub("V","[VN]",ss)
  ss<-gsub("B","[BN]",ss)
  ss<-gsub("H","[HN]",ss)
  ss<-gsub("W","[WHDN]",ss)
  ss<-gsub("S","[SBVN]",ss)
  ss<-gsub("K","[KBDN]",ss)
  ss<-gsub("M","[MHVN]",ss)
  ss<-gsub("Y","[YHBN]",ss)
  ss<-gsub("R","[RVDN]",ss)
  ss<-gsub("C","[CYMSHBVN]",ss)
  ss<-gsub("G","[GRKSBVDN]",ss)
  ss<-gsub("T","[TYKWHBDN]",ss)
  ss<-gsub("A","[ARMWHVDN]",ss)
  return(ss)
}
get_degenerate_bases<-function(s){
  ss<-gsub("R","[AGR]",s)
  ss<-gsub("Y","[CTY]",ss)
  ss<-gsub("M","[ACM]",ss)
  ss<-gsub("K","[GTK]",ss)
  ss<-gsub("S","[GCS]",ss)
  ss<-gsub("W","[ATW]",ss)
  ss<-gsub("H","[ATCMWYH]",ss)
  ss<-gsub("B","[GTCKYSB]",ss)
  ss<-gsub("V","[GACRMSV]",ss)
  ss<-gsub("D","[GATRKWD]",ss)
  ss<-gsub("N","[ATCGRYMKSWHBVDN]",ss)
  return(ss)
}