
####   Paper 
####   Psychologists are open to change, yet wary of rules
####   Heather Fuchs, Mirjam Jenny, & Susann Fiedler

####   Studies 1
####   Submission 1
####   Revision 1

####   Files used:   1)  "FuchsJennyFiedler2012[rawdata].csv" 2) "FuchsJennyFiedler2012[dummy].csv" 3) "FuchsJennyFiedler2012[guidelines].csv"

#### References: Kruschke, J. K. (2011). Doing Bayesian data analysis: A tutorial with R and BUGS. Oxford, England: Academic Press.
#                Hadfield, J. (2011). MCMCglmm Course Notes. Available at http://cran.r-project.org/web/packages/MCMCglmm/


#################
####MAIN TEXT####	
#################

#This code provides all analyses that were conducted using Bayesian statistics.
#The proportions of "yes", "no", and "don't know" answers were computed via beta- and dirichlet-distributions. In this case the solution is analytical.
#The percentages were sampled using normal distributions.
#First, some demographics are provided.
#Note that in order to work all codes needed for these analyses must be located in the same folder, which is defined as the working directory.

#clear workspace
rm(list=ls(all=TRUE))

#load relevant R packages
library(MCMCpack)
library(Hmisc)
library(foreign)
library(coda)
library(languageR)
library(MCMCglmm)
library(R2jags)

#set working directory and load data
mydata=as.data.frame(read.csv(file="FuchsJennyFiedler2012[rawdata].csv", header = TRUE, sep = ","))
mydata <- mydata[-dim(mydata)[1],]


##################
###Demographics###
##################


#number of participants
N=dim(mydata)[1]

#number of countries
Ncountries=length(unique(mydata$v_41)) 

#proportion of female respondents
gender_female=round(sum(mydata$male_yes==2,na.rm=T)/length(mydata$male_yes),2)

#age
mean_age=round(mean(mydata$age[mydata$age>=0],na.rm=T),1) 

sd_age=round(sd(mydata$age[mydata$age>=0],na.rm=T),1) 


#######################
###Bayesian Analyses###
#######################


##### What percentage of respondents agreed that at least one of the recommendations should be followed? #####
RecsFollowed <- cbind(mydata$R1_A,mydata$R2_A,mydata$R3_A,mydata$R4_A,mydata$R5_A,mydata$R6_A)
yes <- RecsFollowed==1
hits <- sum(apply(yes,1,sum)>0) #get the number of positive answers
number <- length(mydata$R1_A) #get the total number of answers
#calculate the posterior binomial beta distribution
binom <- MCbinomialbeta(y=hits, n=number, alpha=1, beta=1, mc=1000000)
mean <- round(mean(binom),2) #get the mean
HDI <- round(coda::HPDinterval(binom),2) #get the HDI


##### What percentage of respondents agreed that at least one of the recommendations should be implemented as a condition for publication? #####
RecsImplemented <- cbind(mydata$R1_B,mydata$R2_B,mydata$R3_B,mydata$R4_B,mydata$R5_B,mydata$R6_B)
yes <- RecsImplemented==1
hits <- sum(apply(yes,1,sum)>0) #get the number of positive answers
number <- length(mydata$R1_A) #get the total number of answers
#calculate the posterior binomial beta distribution
binom <- MCbinomialbeta(y=hits, n=number, alpha=1, beta=1, mc=1000000)
mean <- round(mean(binom),2) #get the mean
HDI <- round(coda::HPDinterval(binom),2) #get the HDI

#Proportion of answers to all recommendations. This code computes posterior distributions and saves their means and HDIs.
#Variables that end in "A" indicate responses to the question "Should researchers follow this recommendation?".
#Variables that end in "B" indicate responses to the question "Should this recommendation be implemented as a recommendation for submissions in psychological journals?".
recs <- cbind(mydata$R1_A,mydata$R1_B,mydata$R2_A,mydata$R2_B,mydata$R3_A,mydata$R3_B,mydata$R4_A,mydata$R4_B,mydata$R5_A,mydata$R5_B,mydata$R6_A,mydata$R6_B) #get respondents answers

freqRecs <- matrix(NA,dim(recs)[2],3) #compute the frequencies of all three answer types per recommendation and question type.
for (i in 1:dim(recs)[2]) {
for (j in 1:3) {
  freqRecs[i,j] <- sum(recs[,i]==j,na.rm=T)
}}
colnames(freqRecs) <- c("Yes","No","Don't know")

tableRecs <- matrix(NA,dim(recs)[2],9) #compute the means and HDIs of the posterior distributions and save them in a table
for (reco in 1:dim(recs)[2]) {
multinom <- MCmultinomdirichlet(y=freqRecs[reco,], alpha0=rep(1,3), mc=1000000)
means <- round(apply(multinom,2,mean)*100)
HDIs <- round(HPDinterval(multinom)*100)
tableRecs[reco,] <- c(means[1],HDIs[1,],means[2],HDIs[2,],means[3],HDIs[3,])
}
colnames(tableRecs) <- c("mYes", "HDIlYes", "HDIhYes","mNo", "HDIlNo", "HDIhNo","mDon't", "HDIlDon't", "HDIhDon't")
rownames(tableRecs) <- c("R1_A","R1_B","R2_A","R2_B","R3_A","R3_B","R4_A","R4_B","R5_A","R5_B","R6_A","R6_B")
save(tableRecs, file="tableRecs.Rdata")


#Proportion of answers to all guidelines (Table 1). This code computes posterior distributions and saves their means and HDIs.
gus <- cbind(mydata$G1,mydata$G2,mydata$G3,mydata$G4) #compute the frequencies of all three answer types per recommendation and question type.
freqGus <- matrix(NA,dim(gus)[2],3)
for (i in 1:4) {
for (j in 1:3) {
  freqGus[i,j] <- sum(gus[,i]==j,na.rm=T)
}}

colnames(freqGus) <- c("Yes","No","Don't know")

tableGuids <- matrix(NA,dim(gus)[2],9)
for (gu in 1:dim(gus)[2]) {
multinom <- MCmultinomdirichlet(y=freqGus[gu,], alpha0=rep(1,3), mc=1000000)
means <- round(apply(multinom,2,mean)*100)
HDIs <- round(HPDinterval(multinom)*100)
tableGuids[gu,] <- c(means[1],HDIs[1,],means[2],HDIs[2,],means[3],HDIs[3,])
}
colnames(tableGuids) <- c("mYes", "HDIlYes", "HDIhYes","mNo", "HDIlNo", "HDIhNo","mDon't", "HDIlDon't", "HDIhDon't")
rownames(tableGuids) <- c("G1","G2","G3","G4")
save(tableGuids, file="tableGuids.Rdata")


##### Were the respondents more likely to agree with the recommendations as standards of good practice as opposed to publication conditions? #####

#load dataset with dummy variables and organize the data
dat=as.data.frame(read.csv(file="FuchsJennyFiedler2012[dummy].csv", header = TRUE, sep = ","))
dat <- as.data.frame(dat)
dat <- dat[dat$position_final<5,]
dat <- dat[dat$subfield<8,]
dat$factorPos <- factor(dat$position_final,labels=c("Phd","Postd","AssP","Ten")) #Reference position: Ph.D.
dat$factorField <- factor(dat$subfield_final,labels=c("Soc","Cog","Jdm","Devep","Neuro","Pers","Clin")) #Reference area: social psychology.

dat <- dat[complete.cases(dat[,c("choice_yes", "Igoodprac1", "Ieditorye2", "factorPos", "factorField", "lfdn", "j")]),]
dat$Ieditorye2 <- ifelse(dat$Ieditorye2==1,0,1)
dat$Igoodprac1 <- ifelse(dat$Igoodprac1==1,0,1)

#put priors on residual variance
priors=list(R = list(V = 1, fix = 1), G = list(G1 = list(V = 1, nu = 0.002),G2 = list(V = 1, nu = 0.002)))  

#sample posterior distributions for three chains
recommendationsBayes1 <- MCMCglmm(choice_yes ~ Igoodprac1 + Ieditorye2 + factorPos + factorField, 
                                  random = ~lfdn + j, data=dat, family="categorical",nitt=100000,burnin=50000,thin=1, prior=priors)

recommendationsBayes2 <- MCMCglmm(choice_yes ~ Igoodprac1 + Ieditorye2 + factorPos + factorField, 
                                  random = ~lfdn + j, data=dat, family="categorical",nitt=100000,burnin=50000,thin=1, prior=priors)

recommendationsBayes3 <- MCMCglmm(choice_yes ~ Igoodprac1 + Ieditorye2 + factorPos + factorField, 
                                  random = ~lfdn + j, data=dat, family="categorical",nitt=100000,burnin=50000,thin=1, prior=priors)  

save(recommendationsBayes1,file="posteriorsRecommendationsBayes1.R")
save(recommendationsBayes2,file="posteriorsRecommendationsBayes2.R")
save(recommendationsBayes3,file="posteriorsRecommendationsBayes3.R")  

#paste chains of the intercept and the predictors together
recsfixed.chains <- mcmc.list(as.mcmc(recommendationsBayes1$Sol), as.mcmc(recommendationsBayes2$Sol),as.mcmc(recommendationsBayes3$Sol))
save(recsfixed.chains,file="logRegrecommendationsFixedEffects.R")

#extract the chains for the fixed effects
recsfixed <- as.mcmc(rbind(recsfixed.chains[[1]],recsfixed.chains[[2]],recsfixed.chains[[3]]))  

#rescale to get similar results as a maximum likelihood regression (residual variance fixed on 0, Hadfield course notes p. 51)
c2 <- ((16 * sqrt(3))/(15 * pi))^2  
recommendations <- recsfixed/sqrt(1 + c2)  
summary(recommendations)  
round(coda::HPDinterval(recommendations),2)

#odds ratio editor:
OR.editor <-   exp(recommendations[,"Ieditorye2"])
summary(OR.editor)
coda::HPDinterval(OR.editor)

#odds ratio format:
OR.format <-   exp(recommendations[,"Igoodprac1"])
summary(OR.format)
coda::HPDinterval(OR.format)   

#paste chains of the intercept and the predictors together
recsrandom.chains <- mcmc.list(as.mcmc(sqrt(recommendationsBayes1$VCV)), as.mcmc(sqrt(recommendationsBayes2$VCV)), as.mcmc(sqrt(recommendationsBayes3$VCV))) #standardabweichung des intercept der random effects, wie stark ist die heterogenität im intercept
save(recsrandom.chains,file="logRegrecommendationsRandomEffects.R")

#extract the chains for the random effects
recsrandom <- as.mcmc(rbind(recsrandom.chains[[1]],recsrandom.chains[[2]],recsrandom.chains[[3]]))

IntraclasscorrelationParticipants <- recsrandom[, 1]/(rowSums(recsrandom) + pi^2/3)  
IntraclasscorrelationItems <- recsrandom[, 2]/(rowSums(recsrandom) + pi^2/3)  
summary(IntraclasscorrelationParticipants)  
summary(IntraclasscorrelationItems)
coda::HPDinterval(IntraclasscorrelationParticipants)
coda::HPDinterval(IntraclasscorrelationItems)



##### What percentage of respondents agreed that at least one of the guidelines should be followed? #####
GuidsFollowed <- cbind(mydata$G1,mydata$G2,mydata$G3,mydata$G4)
yes <- GuidsFollowed==1
hits <- sum(apply(yes,1,sum)>0) #get the number of positive answers
number <- length(mydata$G1) #get the total number of answers
#calculate the posterior binomial beta distribution
binom <- MCbinomialbeta(y=hits, n=number, alpha=1, beta=1, mc=1000000)
mean <- round(mean(binom),2) #get the mean
HDI <- round(coda::HPDinterval(binom),2) #get the HDI


##### What percentage of print and online journal space should be dedicated to novel studies and what percentage to direct replications? #####
##### What percentage of results in psychology as a whole and in the respondents' specific area could be replicated in direct replications? #####
##### These analyses require the open source software Just Another Gibbs Sampler. The code for the Bayesian model is adapted from John Kruschke's YmetricXsingleJags.R file.
mydata=as.data.frame(read.csv(file="FuchsJennyFiedler2012[rawdata].csv", header = TRUE, sep = ","))
attach(mydata)

#exclude participants who answered with "0" to all of these variables
dropPartic = 
  which(
    round(novel_online, 6) == 0 &
      round(novel_print, 6) == 0 &
      round(preplication_print, 6) == 0 &
      round(replication_online, 6) == 0 &
      round(reproducability, 6) == 0 &
      round(reproducability_spec, 6) == 0
  )

includePart = (1:nrow(mydata))[-dropPartic]
mydata = mydata[includePart,]

detach(mydata)

# -> here choose (uncomment) the relevant one and perform the analyses below:
#replic <- mydata$reproducability_spec
#replic <- mydata$reproducability
#replic <- mydata$novel_print
#replic <- mydata$novel_online
#replic <- mydata$preplication_print 
#replic <- mydata$replication_online

replic <- replic[complete.cases(replic)]
replic <- replic[replic < 101] #exclude answers above 100%
N=length(replic)

data  = list("N","replic") #prepare data and pass it to JAGS

#define initial values
myinits = list(
  list(mu= mean(replic), tau= 1 / sd( replic )^2), 
  list(mu= 0, tau= (1 / sd( replic )^2)/100), 
  list(mu= 100, tau= (1 / sd( replic )^2)*100)
)

# parameters to be monitored
parameters = c("mu", "tau")


samples = jags(data, inits=myinits, parameters,
               model.file ="normalDist.txt",
               n.chains=3, n.iter=20000, n.burnin=10000, n.thin=1,
               DIC=T)

# Assess the convergence with the coda package
library(coda)
library(MCMCglmm)
coda.c1 = as.mcmc(samples$BUGSoutput$sims.array[,1,"mu"])
coda.c2 = as.mcmc(samples$BUGSoutput$sims.array[,2,"mu"])
coda.c3 = as.mcmc(samples$BUGSoutput$sims.array[,3,"mu"])
coda.c  = mcmc.list(coda.c1,coda.c2,coda.c3)
traceplot(coda.c)

#extract the mean and HDI
mean <- mean(replic)
HDI <- round(HPDinterval(as.mcmc(unlist(coda.c))))



#################
#######SOM#######  
#################




##### Did fewer respondents answer yes to the last recommendation than to the first? #####
mydata=as.data.frame(read.csv(file="FuchsJennyFiedler2012[rawdata].csv", header = TRUE, sep = ","))
mydata <- mydata[-dim(mydata)[1],]

#extract respondents' answers to the first recommendation
propYes1  <- array(NA,3)
for (i in 1:3) {
  propYes1[i] <- sum(mydata$AnsRec1==i,na.rm=T)
}

#summarize respondents' answers in a table
propYes1 <- table(mydata$AnsRec1)

#calculate the posterior distributions of the proportions
multinom1 <- MCmultinomdirichlet(y=propYes1, alpha0=rep(1,3), mc=1000000)
summary(multinom1) #inspect the summary statistics
HPDinterval(multinom1) #inspect the HDI

#summarize respondents' answers to the last recommendation
propYesl <- table(mydata$AnsRec10)

#calculate the posterior distributions of the proportion
multinoml <- MCmultinomdirichlet(y=propYesl, alpha0=rep(1,3), mc=1000000)
summary(multinoml)  #inspect the summary statistics
HPDinterval(multinoml) #inspect the HDI

HPDinterval(multinom1[,1]-multinoml[,1]) #inspect the HDI of the difference


##### Did current position, field of research, experience as an editor, or agreement type predict agreement with the recommendations? #####
dat=as.data.frame(read.csv(file="FuchsJennyFiedler2012[dummy].csv", header = TRUE, sep = ","))
dat <- as.data.frame(dat)
dat <- dat[dat$position_final<5,]
dat <- dat[dat$subfield<8,]
dat$factorPos <- factor(dat$position_final,labels=c("Phd","Postd","AssP","Ten")) #reference position: Ph.D. 
dat$factorField <- factor(dat$subfield_final,labels=c("Soc","Cog","Jdm","Devep","Neuro","Pers","Clin")) #reference area: social psychology


dat <- dat[complete.cases(dat[,c("choice_yes", "Igoodprac1", "Ieditorye2", "factorPos", "factorField", "lfdn", "j")]),]

dat$Ieditorye2 <- ifelse(dat$Ieditorye2==1,0,1) #reference class non-editors

dat$Igoodprac1 <- ifelse(dat$Igoodprac1==1,0,1) #reference class good practice

#put priors on residual variance
priors=list(R = list(V = 1, fix = 1), G = list(G1 = list(V = 1, nu = 0.002),G2 = list(V = 1, nu = 0.002)))  

#sample posterior distributions for three chains
recommendationsBayes1 <- MCMCglmm(choice_yes ~ Igoodprac1 + Ieditorye2 + factorPos + factorField, 
                                  random = ~lfdn + j, data=dat, family="categorical",nitt=100000,burnin=50000,thin=1, prior=priors)

recommendationsBayes2 <- MCMCglmm(choice_yes ~ Igoodprac1 + Ieditorye2 + factorPos + factorField, 
                                  random = ~lfdn + j, data=dat, family="categorical",nitt=100000,burnin=50000,thin=1, prior=priors)

recommendationsBayes3 <- MCMCglmm(choice_yes ~ Igoodprac1 + Ieditorye2 + factorPos + factorField, 
                                  random = ~lfdn + j, data=dat, family="categorical",nitt=100000,burnin=50000,thin=1, prior=priors)  

save(recommendationsBayes1,file="posteriorsRecommendationsBayes1.R")
save(recommendationsBayes2,file="posteriorsRecommendationsBayes2.R")
save(recommendationsBayes3,file="posteriorsRecommendationsBayes3.R")  

#paste chains of the intercept and the predictors together
recsfixed.chains <- mcmc.list(as.mcmc(recommendationsBayes1$Sol), as.mcmc(recommendationsBayes2$Sol),as.mcmc(recommendationsBayes3$Sol))
save(recsfixed.chains,file="logRegrecommendationsFixedEffects.R")

#extract the chains for the fixed effects
recsfixed <- as.mcmc(rbind(recsfixed.chains[[1]],recsfixed.chains[[2]],recsfixed.chains[[3]]))  

#rescale to get similar results as a maximum likelihood regression (residual variance fixed on 0, Hadfield course notes p. 51)
c2 <- ((16 * sqrt(3))/(15 * pi))^2  
recommendations <- recsfixed/sqrt(1 + c2)  
summary(recommendations)  
round(coda::HPDinterval(recommendations),2)

#odds ratio intercept:
inter <- mean(recommendations[,"(Intercept)"])  
coda::HPDinterval((recommendations[,"(Intercept)"]))  

OR.intercept <- exp(recommendations[,"(Intercept)"])
summary(OR.intercept)
coda::HPDinterval(OR.intercept)  

OR.intercept <- (recommendations[,"(Intercept)"])
exp(mean(OR.intercept))
exp(coda::HPDinterval(OR.intercept) )

#odds ratio editor:
OR.editor <-   exp(recommendations[,"Ieditorye2"])
summary(OR.editor)
coda::HPDinterval(OR.editor)

OR.editor <-   (recommendations[,"Ieditorye2"])
exp(mean(OR.editor))
exp(coda::HPDinterval(OR.editor)  )

#odds ratio format:
OR.format <-   exp(recommendations[,"Igoodprac1"])
summary(OR.format)
coda::HPDinterval(OR.format)  

OR.format <-   (recommendations[,"Igoodprac1"])
exp(mean(OR.format))
exp(coda::HPDinterval(OR.format)  )

#odds ratio Postdoc:
OR.Postdoc <-   exp(recommendations[,"factorPosPostd"])
summary(OR.Postdoc)
coda::HPDinterval(OR.Postdoc)  

OR.Postdoc <-   (recommendations[,"factorPosPostd"])
exp(mean(OR.Postdoc))
exp(coda::HPDinterval(OR.Postdoc))

#odds ratio AssProf:
OR.AssProf <-   exp(recommendations[,"factorPosAssP"])
summary(OR.AssProf)
coda::HPDinterval(OR.AssProf)

OR.AssProf <-   (recommendations[,"factorPosAssP"])
exp(mean(OR.AssProf))
exp(coda::HPDinterval(OR.AssProf))

#odds ratio Tenured Prof:
OR.Ten <-   exp(recommendations[,"factorPosTen"])
summary(OR.Ten)
coda::HPDinterval(OR.Ten)

OR.Ten <-   (recommendations[,"factorPosTen"])
exp(mean(OR.Ten))
exp(coda::HPDinterval(OR.Ten))

#odds ratio field cog psych:
OR.Cog <-   exp(recommendations[,"factorFieldCog"])
summary(OR.Cog)
coda::HPDinterval(OR.Cog)

OR.Cog <-   (recommendations[,"factorFieldCog"])
exp(mean(OR.Cog))
exp(coda::HPDinterval(OR.Cog))

#odds ratio field JDM psych:
OR.JDM <-   exp(recommendations[,"factorFieldJdm"])
summary(OR.JDM)
coda::HPDinterval(OR.JDM)

OR.JDM <-   (recommendations[,"factorFieldJdm"])
exp(mean(OR.JDM))
exp(coda::HPDinterval(OR.JDM))

#odds ratio field developmental psych:
OR.dev <-   exp(recommendations[,"factorFieldDevep"])
summary(OR.dev)
coda::HPDinterval(OR.dev)

OR.dev <-   (recommendations[,"factorFieldDevep"])
exp(mean(OR.dev))
exp(coda::HPDinterval(OR.dev))

#odds ratio field neuro:
OR.neur <-   exp(recommendations[,"factorFieldNeuro"])
summary(OR.neur)
coda::HPDinterval(OR.neur)

OR.neur <-   (recommendations[,"factorFieldNeuro"])
exp(mean(OR.neur))
exp(coda::HPDinterval(OR.neur))

#odds ratio field pers:
OR.pers <-   exp(recommendations[,"factorFieldPers"])
summary(OR.pers)
coda::HPDinterval(OR.pers)

OR.pers <-   (recommendations[,"factorFieldPers"])
exp(mean(OR.pers))
exp(coda::HPDinterval(OR.pers))

#odds ratio field clin:
OR.clin <-   exp(recommendations[,"factorFieldClin"])
summary(OR.clin)
coda::HPDinterval(OR.clin)

OR.clin <-   (recommendations[,"factorFieldClin"])
exp(mean(OR.clin))
exp(coda::HPDinterval(OR.clin)  )


#paste chains of the intercept and the predictors together
recsrandom.chains <- mcmc.list(as.mcmc(sqrt(recommendationsBayes1$VCV)), as.mcmc(sqrt(recommendationsBayes2$VCV)), as.mcmc(sqrt(recommendationsBayes3$VCV)))
save(recsrandom.chains,file="logRegrecommendationsRandomEffects.R")

#extract the chains for the random effects
recsrandom <- as.mcmc(rbind(recsrandom.chains[[1]],recsrandom.chains[[2]],recsrandom.chains[[3]]))

IntraclasscorrelationParticipants <- recsrandom[, 1]/(rowSums(recsrandom) + pi^2/3)  
IntraclasscorrelationItems <- recsrandom[, 2]/(rowSums(recsrandom) + pi^2/3)  
summary(IntraclasscorrelationParticipants)  
summary(IntraclasscorrelationItems)
coda::HPDinterval(IntraclasscorrelationParticipants)
coda::HPDinterval(IntraclasscorrelationItems)


##### Did current position, field of research, experience as an editor or agreement type predict agreement with the guidelines? #####
dat <- as.data.frame(read.csv(file="FuchsJennyFiedler2012[guidelines].csv", header = TRUE, sep = ","))
dat <- dat[dat$position_final<5,]
dat <- dat[dat$subfield<8,]
dat$factorPos <- factor(dat$position_final,labels=c("Phd","Postd","AssP","Ten")) #reference position: Ph.D. 
dat$factorField <- factor(dat$subfield_final,labels=c("Soc","Cog","Jdm","Devep","Neuro","Pers","Clin")) #reference area: social psychology

dat <- dat[complete.cases(dat[,c("choice_yesG", "Ieditorye2", "factorPos", "factorField", "lfdn", "j")]),]
dat$Ieditorye2 <- ifelse(dat$Ieditorye2==1,0,1) #now the reference class is non-editors


#put priors on residual variance
priors=list(R = list(V = 1, fix = 1), G = list(G1 = list(V = 1, nu = 0.002),G2 = list(V = 1, nu = 0.002)))  

#sample posterior distributions for three chains
guidelinesBayes1 <- MCMCglmm(choice_yesG ~ Ieditorye2 + factorPos + factorField, 
                             random = ~lfdn + j, data=dat, family="categorical",nitt=100000,burnin=50000,thin=1, prior=priors)
guidelinesBayes2 <- MCMCglmm(choice_yesG ~ Ieditorye2 + factorPos + factorField, 
                             random = ~lfdn + j, data=dat, family="categorical",nitt=100000,burnin=50000,thin=1, prior=priors)
guidelinesBayes3 <- MCMCglmm(choice_yesG ~ Ieditorye2 + factorPos + factorField, 
                             random = ~lfdn + j, data=dat, family="categorical",nitt=100000,burnin=50000,thin=1, prior=priors)

save(guidelinesBayes1,file="posteriorsGuidelinesBayes1.R")
save(guidelinesBayes2,file="posteriorsGuidelinesBayes2.R")
save(guidelinesBayes3,file="posteriorsGuidelinesBayes3.R")

#paste chains of the intercept and the predictors together
recsfixed.chains <- mcmc.list(as.mcmc(guidelinesBayes1$Sol), as.mcmc(guidelinesBayes2$Sol),as.mcmc(guidelinesBayes3$Sol))
save(recsfixed.chains,file="logRegguidelinesFixedEffects.R")

#extract the chains for the fixed effects
recsfixed <- as.mcmc(rbind(recsfixed.chains[[1]],recsfixed.chains[[2]],recsfixed.chains[[3]]))  

#rescale to get similar results as a maximum likelihood regression (residual variance fixed on 0, Hadfield course notes p. 51)
c2 <- ((16 * sqrt(3))/(15 * pi))^2  
guidelines <- recsfixed/sqrt(1 + c2)  
summary(guidelines)  
round(coda::HPDinterval(guidelines),2)

#odds ratio intercept:
inter <- mean(guidelines[,"(Intercept)"])  
coda::HPDinterval((guidelines[,"(Intercept)"]))

OR.intercept <- exp(guidelines[,"(Intercept)"])
summary(OR.intercept)
coda::HPDinterval(OR.intercept)

OR.intercept <- (guidelines[,"(Intercept)"])
exp(mean(OR.intercept))
exp(coda::HPDinterval(OR.intercept))

#odds ratio editor:
OR.editor <-   exp(guidelines[,"Ieditorye2"])
summary(OR.editor)
coda::HPDinterval(OR.editor)

OR.editor <-   (guidelines[,"Ieditorye2"])
exp(mean(OR.editor))
exp(coda::HPDinterval(OR.editor))


#odds ratio Postdoc:
OR.Postdoc <-   exp(guidelines[,"factorPosPostd"])
summary(OR.Postdoc)
coda::HPDinterval(OR.Postdoc)  

OR.Postdoc <-   (guidelines[,"factorPosPostd"])
exp(mean(OR.Postdoc))
exp(coda::HPDinterval(OR.Postdoc))

#odds ratio AssProf:
OR.AssProf <-   exp(guidelines[,"factorPosAssP"])
summary(OR.AssProf)
coda::HPDinterval(OR.AssProf)

OR.AssProf <-   (guidelines[,"factorPosAssP"])
exp(mean(OR.AssProf))
exp(coda::HPDinterval(OR.AssProf))

#odds ratio Tenured Prof:
OR.Ten <-   exp(guidelines[,"factorPosTen"])
summary(OR.Ten)
coda::HPDinterval(OR.Ten)

OR.Ten <-   (guidelines[,"factorPosTen"])
exp(mean(OR.Ten))
exp(coda::HPDinterval(OR.Ten))

#odds ratio field cog psych:
OR.Cog <-   exp(guidelines[,"factorFieldCog"])
summary(OR.Cog)
coda::HPDinterval(OR.Cog)

OR.Cog <-   (guidelines[,"factorFieldCog"])
exp(mean(OR.Cog))
exp(coda::HPDinterval(OR.Cog))

#odds ratio field JDM psych:
OR.JDM <-   exp(guidelines[,"factorFieldJdm"])
summary(OR.JDM)
coda::HPDinterval(OR.JDM)

OR.JDM <-   (guidelines[,"factorFieldJdm"])
exp(mean(OR.JDM))
exp(coda::HPDinterval(OR.JDM))

#odds ratio field developmental psych:
OR.dev <-   exp(guidelines[,"factorFieldDevep"])
summary(OR.dev)
coda::HPDinterval(OR.dev)

OR.dev <-   (guidelines[,"factorFieldDevep"])
mean(exp(OR.dev))
exp(coda::HPDinterval(OR.dev))

#odds ratio field neuro:
OR.neur <-   exp(guidelines[,"factorFieldNeuro"])
summary(OR.neur)
coda::HPDinterval(OR.neur)

OR.neur <-   (guidelines[,"factorFieldNeuro"])
exp(mean(OR.neur))
exp(coda::HPDinterval(OR.neur))

#odds ratio field pers:
OR.pers <-   exp(guidelines[,"factorFieldPers"])
summary(OR.pers)
coda::HPDinterval(OR.pers)

OR.pers <-   (guidelines[,"factorFieldPers"])
exp(mean(OR.pers))
exp(coda::HPDinterval(OR.pers))

#odds ratio field clin:
OR.clin <-   exp(guidelines[,"factorFieldClin"])
summary(OR.clin)
coda::HPDinterval(OR.clin)

OR.clin <-   (guidelines[,"factorFieldClin"])
exp(mean(OR.clin))
exp(coda::HPDinterval(OR.clin))

#paste chains of the intercept and the predictors together
recsrandom.chains <- mcmc.list(as.mcmc(sqrt(guidelinesBayes1$VCV)), as.mcmc(sqrt(guidelinesBayes2$VCV)), as.mcmc(sqrt(guidelinesBayes3$VCV))) 
save(recsrandom.chains,file="logRegguidelinesRandomEffects.R")

#extract the chains for the random effects

IntraclasscorrelationParticipants <- recsrandom[, 1]/(rowSums(recsrandom) + pi^2/3)  
IntraclasscorrelationItems <- recsrandom[, 2]/(rowSums(recsrandom) + pi^2/3)  
summary(IntraclasscorrelationParticipants)  
summary(IntraclasscorrelationItems)
coda::HPDinterval(IntraclasscorrelationParticipants)
coda::HPDinterval(IntraclasscorrelationItems)

