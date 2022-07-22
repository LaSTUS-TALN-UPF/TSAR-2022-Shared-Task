# -*- coding: utf-8 -*-

# Official evaluation script for TSAR-2022 Shared Task on Lexical Simplification for English, Portuguese and Spanish.
# site: https://taln.upf.edu/pages/tsar2022-st/



import sys
from optparse import OptionParser
import math


class TSAR2022_SharedTask_Evaluator(object):

    def __init__(self,output_file,verbose):
        self.verbose=verbose
        self.output_file=output_file
        self.combined = None
        self.goldinfo = None
        self.flagUseComplexWordsInGoldAnnotations=False
        

        
    def match(self,label, gold_annotation):

        if label == gold_annotation:
            return True
        return False

        
    
        
    def match_group(self,label, gold_annotations):
        
        for g in gold_annotations:
            if self.match(label, g):
                return True
        return False


    def match_group_to_group(self,list_labels, gold_annotations):
        
        for label in list_labels:
            if self.match_group(label, gold_annotations):
                return True
        return False
    
    

    def read_files(self,gold_file, labels_file):

        self.gold_file=gold_file
        self.labels_file=labels_file
        
        if self.verbose:
            print("______________________________________________________")
            print("gold_file:",gold_file)
            print("labels_file:",labels_file)
            print("______________________________________________________")
        
        # Read files
        gold_lines = open(gold_file,'r').readlines()
        labels_lines = open(labels_file,'r').readlines()
        
        
        self.goldinfo={}
        
        if self.verbose:
            print("______________________________________________________")
            print("_____________ GOLD ANNOTATIONS FILE __________________")
            print("______________________________________________________")
        
        
        for line in gold_lines:
            split = line.strip().split("\t")
            keygold = split[0] + "__" + split[1]
            
            complex_word=split[1]
            
            if self.verbose:
                print("keygold:", keygold)
            
            
            items = [item.strip() for item in split[2:]]
            
            if self.verbose:
                print("items:", items)
            
            dict_items={}
            
            for item in items:
                
                if self.flagUseComplexWordsInGoldAnnotations==False:
                
                
                    if item!=complex_word:
                        if item in dict_items.keys():
                            dict_items[item]+=1
                        else:
                            dict_items[item]=1
                        
                else:
                    
                    if item in dict_items.keys():
                        dict_items[item]+=1
                    else:
                        dict_items[item]=1
                        
                        
            if self.verbose:
                print("goldinfo ITEMS:", dict_items)
                    
            
            dict_values_items={}
            
            for value in dict_items.values():
                dict_values_items[value]=[]
            
            for k in dict_items.keys():
                if k not in dict_values_items[dict_items[k]]:
                    dict_values_items[dict_items[k]].append(k)
            
            list_num_counts_items=sorted(dict_values_items.keys())
            list_num_counts_items.reverse()
                        
            if self.verbose:
                print("list_num_counts_items:", list_num_counts_items)
            
            list_values_items_lists=[]
            for key in list_num_counts_items:
                list_values_items_lists.append(dict_values_items[key])
    
            
            if self.verbose:
                print("list_values_items_lists:", list_values_items_lists)
            
            
            self.goldinfo[keygold] = {'gold': dict_items.keys(), 'list_values': list_num_counts_items,'list_keys_lists':list_values_items_lists}

            
            if self.verbose:
                print("goldinfo:", self.goldinfo[keygold])
                print("______________________________________________________")
            
        
        
        
        
        
        self.combined={}

        
        if self.verbose:
            print("______________________________________________________")
            print("_____________ PREDICTIONS FILE _______________________")
            print("______________________________________________________")
        

        for line in labels_lines:
            split = line.strip().split("\t")
            key = split[0] + "__" + split[1]
            items = [item.strip() for item in split[2:]]
            
            
            
            if self.verbose:
                print("______________________________________________________")
                print("original_items:", items)
            
            
            #filtering out complex words in the predicted labels and repeated predictions
            complex_word=split[1]
            filtered_items=[]
            
            for item in items:
                if item not in filtered_items and not item==complex_word:
                    filtered_items.append(item) 
            
            
            if self.verbose:
                print("filtered_items:", filtered_items)
                print("______________________________________________________")
            
            
            
            self.combined[key] = { 'labels': filtered_items }

        
    
        
        
        
    def computeAccuracy_at_1(self):
        
        # Accuracy Metric

        if self.verbose:
            print()
            print()
            print("############################")
            print("    Accuracy Metric ACC@1")
            print("############################")
            print()
            print("______________________________________________________")

        tp = 0
        total = 0

        for key in self.combined.keys():
            
            
            if self.combined[key]['labels']!=None and len(self.combined[key]['labels'])>0:
                if self.verbose:
                    print("______________________________________________________")
                    print("Context = " + str(self.combined[key]))
                    print("Gold  = ",self.goldinfo[key]['gold'])
                    print("Label = ",self.combined[key]['labels'])
                    print("Label topk=1 =",self.combined[key]['labels'][0])
    
                    
                sentence,complexWord=key.split('__')
                if self.match_group(self.combined[key]['labels'][0],self.goldinfo[key]['gold']):
                    if self.verbose:
                        print("MATCH @acc1_set_gold=",self.combined[key]['labels'][0])
                        print("______________________________________________________")
                    tp += 1
                elif self.verbose:
                        print("NO MATCH\n")
                        print("______________________________________________________")
                        

            total += 1

            
        if self.verbose:
            print("TOTALMATCHES acc@1: ",str(tp))
            print("______________________________________________________")
            
        accuracy = tp/total
                   
        return accuracy


    def computeAccuracy_at_N_at_top_gold_1(self,N):
        
        # Accuracy Metric

        if self.verbose:
            print()
            print()
            print("#############################################")
            print("    Accuracy Metric @",N,"@ GOLD FIRST MATCH")
            print("#############################################")
            print()
            print("______________________________________________________")

        tp = 0
        total = 0

        for key in self.combined.keys():

            if self.combined[key]['labels']!=None and len(self.combined[key]['labels'])>0:

            
                if self.verbose:
                    print("______________________________________________________")
                    print("Context = " + str(self.combined[key]))
                    print("Gold  = ",self.goldinfo[key]['gold'])
                    print("Label = ",self.combined[key]['labels'])
                    print("Label topN=",N," ",self.combined[key]['labels'][0:N])
                    print("Gold topk=1 list =", self.goldinfo[key]['list_keys_lists'][0])
                    
    
                sentence,complexWord=key.split('__')
                if self.match_group_to_group(self.combined[key]['labels'][0:N],self.goldinfo[key]['list_keys_lists'][0]):
                    if self.verbose:
                        print("MATCH acc@N_gold_first=",self.combined[key]['labels'][0:N])
                        print("______________________________________________________")
                    tp += 1
                elif self.verbose:
                        print("NO MATCH\n")
                        print("______________________________________________________")
                        

            total += 1

        
        
        if self.verbose:    
            print("TOTALMATCHES accuracy@",N,"_at_top_gold_1:",str(tp))
            print("______________________________________________________")
            
        accuracy = tp/total
                   
        return accuracy

  
   
    
    
    def computePrecisionMetrics_at_K(self,K):
                   
        # Precision

        if self.verbose:
            print()
            print()
            print("##############################################################################################")
            print("     Potential, MicroAverage and MacroAverage Precision, Recall and F1 Metrics at ",K)
            print("##############################################################################################")
            print()


        MacroAverage_Precision = 0
        MicroAverage_Precision = 0
        MacroAverage_Recall = 0
        MicroAverage_Recall = 0
        MacroAverage_F1 = 0
        MicroAverage_F1 = 0

        running_precision = 0
        total_counts_precision=0
        running_recall = 0
        total_counts_recall=0
        total_counts_labels=0

        potential_counts=0
        Potential=0

        total = 0

        for key in self.combined.keys():
            
            
            if self.combined[key]['labels']!=None and len(self.combined[key]['labels'])>0:

                if self.verbose:
                    print("______________________________________________________")
                    print("Context = " + str(self.combined[key]))
                    print("Gold  = " + str(self.goldinfo[key]['gold']))
                    print("Label = " + str(self.combined[key]['labels']))
    
                gold_annotations= self.goldinfo[key]['gold']
                
                labels = self.combined[key]['labels'][0:K]
    
                total_counts_labels+=len(labels)
    
                sentence,complexWord=key.split('__')
                acc_labels = [l for l in labels if self.match_group( l, gold_annotations)]
                acc_gold = [l for l in gold_annotations if self.match_group(l, labels)]
    
    
                total_counts_precision+=len(acc_labels)
    
                if len(acc_labels)>0:
                    potential_counts+=1
    
                total_counts_recall+=len(acc_gold)
    
                precision = len(acc_labels) / len(labels)
                recall = len(acc_gold) / len(gold_annotations)
    
    
                if self.verbose:
                    print("Matched Labels with respect Gold = " +str(acc_labels))
                    print("Matched Gold with respect Labels = " +str(acc_gold))
                    print("Precision = " + str(precision))
                    print("Recall = " + str(recall)+"\n")
                    print("______________________________________________________")
                    
    
                running_precision += precision
                running_recall += recall

            total += 1

        MacroAverage_Precision = running_precision / total
        MacroAverage_Recall = running_recall / total


        if total_counts_labels>0:
            
            MicroAverage_Precision= total_counts_precision / total_counts_labels
            MicroAverage_Recall = total_counts_recall / total_counts_labels
            
            

        MacroAverage_F1=0
        MicroAverage_F1=0


        if (MacroAverage_Precision+MacroAverage_Recall)>0:
                    MacroAverage_F1 = 2*MacroAverage_Precision*MacroAverage_Recall/(MacroAverage_Precision+MacroAverage_Recall)
                    MicroAverage_F1 = 2*MicroAverage_Precision*MicroAverage_Recall/(MicroAverage_Precision+MicroAverage_Recall)

        if (potential_counts>0):
            Potential=potential_counts/total

                   
                   
                   
        return MacroAverage_Precision,MacroAverage_Recall,MacroAverage_F1,MicroAverage_Precision,MicroAverage_Recall,MicroAverage_F1, Potential


               
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
                   
    #Mean Average Precision
    # Parameters : 
    #  1. List of Binary Relevance Judgments e.g. [False, True, True, False, False]
    #  2. K
    

    def MAP_at_K(self,list_gold_items_match,K):
        MAP = 0
        AP = 0

        TruePositivesSeen=0
        index=0

        
        list_precision_calculations=[]
        for item in list_gold_items_match:
            index+=1
            if index>K:
                break
            if item==True:
                TruePositivesSeen+=1
                precision=TruePositivesSeen/index
                list_precision_calculations.append(precision)
                AP+=precision
            
            else:
                list_precision_calculations.append(0)
            

        MAP=AP/K

        
        if self.verbose:
            print("list_precision_calculations:", list_precision_calculations)
            print("AP:", AP)
            print("K:", K)
            print("MAP:", MAP)
            print("______________________________________________________")
        
        
        return MAP

                   
                   
                   
    def computeMAP_at_K(self,K):

        # MAP metric

        if self.verbose:
            print()
            print()
            print("###########################################################################")
            print("         MeanAveragePrecision (MAP) metric @",K)
            print("###########################################################################")
            print()
    
        total_instances=0   
        MAP_global_accumulator=0
        MAP=0          

        
    
        for key in self.combined.keys():
            if self.verbose:
                print("______________________________________________________")
                print("Context = " + str(self.combined[key]))
                print("Gold  = " + str(self.goldinfo[key]['gold']))
                print("Label = " + str(self.combined[key]['labels']))

            gold = set(self.goldinfo[key]['gold'])
            labels = set(self.combined[key]['labels'])

            list_labels=self.combined[key]['labels']
            gold_annotations=self.goldinfo[key]['gold']


            #########################################
            # MAP 
            #########################################

            
            if self.verbose:
                print("MAP")
                print("labels:",list_labels)
                print("gold:", gold_annotations)

            
            sentence,complexWord=key.split('__')

            labels_relevance_judgements=[]
            for label in list_labels:
                labels_relevance_judgements.append(self.match_group(label, gold_annotations))

            if self.verbose:
                print("labels_relevance_judgements:")
                print(labels_relevance_judgements)

            MAP_local=self.MAP_at_K(labels_relevance_judgements,K)
            MAP_global_accumulator+=MAP_local
            total_instances+=1 
                   
                   
                   
        if (MAP_global_accumulator>0):
    
            MAP=MAP_global_accumulator/total_instances
           
        return MAP       



                   
    def print_output_results(self, Potential_at_1,
                                   Potential_at_3,
                                   Potential_at_5,
                                   Potential_at_10,
                                   MAP_at_3,
                                   MAP_at_5,
                                   MAP_at_10,
                                   Accuracy_at_1_at_top_gold_1,
                                   Accuracy_at_2_at_top_gold_1,
                                   Accuracy_at_3_at_top_gold_1):
        
    

        
        print("=========   EVALUATION config.=========")
                   
        print('GOLD file = ' + str(self.gold_file))
        print('PREDICTION LABELS file = ' + str(self.labels_file))
        print('OUTPUT file = ' + str(self.output_file))
        print("===============   RESULTS  =============\n")
    
    
    
        print('MAP@1/Potential@1/Precision@1 = ' + str(Potential_at_1)+"\n")
    
        print('MAP@3 = ' + str(MAP_at_3))
        print('MAP@5 = ' + str(MAP_at_5))
        print('MAP@10 = ' + str(MAP_at_10)+"\n")

        print('Potential@3 = ' + str(Potential_at_3))
        print('Potential@5 = ' + str(Potential_at_5))
        print('Potential@10 = ' + str(Potential_at_10)+"\n")
        
        
        print('Accuracy@1@top_gold_1 = ' + str(Accuracy_at_1_at_top_gold_1))
        print('Accuracy@2@top_gold_1 = ' + str(Accuracy_at_2_at_top_gold_1))
        print('Accuracy@3@top_gold_1 = ' + str(Accuracy_at_3_at_top_gold_1))
        print('\n')
    
    
    
    
    def write_output_results(self, Potential_at_1,
                                   Potential_at_3,
                                   Potential_at_5,
                                   Potential_at_10,
                                   MAP_at_3,
                                   MAP_at_5,
                                   MAP_at_10,
                                   Accuracy_at_1_at_top_gold_1,
                                   Accuracy_at_2_at_top_gold_1,
                                   Accuracy_at_3_at_top_gold_1):
        
    
    
    
        out_file = open(self.output_file,mode='w',encoding='utf-8')
    
    
        out_file.write("=========   EVALUATION config.=========\n")
                       
        out_file.write('GOLD file = ' + str(self.gold_file)+'\n')
        out_file.write('PREDICTION LABELS file = ' + str(self.labels_file)+'\n')
        out_file.write('OUTPUT file = ' + str(self.output_file)+'\n')
        out_file.write("===============   RESULTS  =============\n")
        
        
        out_file.write('MAP@1/Potential@1/Precision@1 = ' + str(Potential_at_1)+'\n\n')
        
    
        out_file.write('MAP@3 = ' + str(MAP_at_3)+'\n')
        out_file.write('MAP@5 = ' + str(MAP_at_5)+'\n')
        out_file.write('MAP@10 = ' + str(MAP_at_10)+'\n\n')
  
        
        out_file.write('Potential@3 = ' + str(Potential_at_3)+'\n')
        out_file.write('Potential@5 = ' + str(Potential_at_5)+'\n')
        out_file.write('Potential@10 = ' + str(Potential_at_10)+'\n\n')
        
        out_file.write('Accuracy@1@top_gold_1 = ' + str(Accuracy_at_1_at_top_gold_1)+'\n')
        out_file.write('Accuracy@2@top_gold_1 = ' + str(Accuracy_at_2_at_top_gold_1)+'\n')
        out_file.write('Accuracy@3@top_gold_1 = ' + str(Accuracy_at_3_at_top_gold_1)+'\n\n')
        
        out_file.write('________________________________\n')
        out_file.close()
    
    
    
  

def main():

    
    # arg parsing
    parser = OptionParser(usage='Evaluation Script for the TSAR-2022 Lexical Simplification Shared Task\n\nUsage: %prog <options>')

    parser.add_option('--gold_file', metavar='<PATH>', action='store', type='string', dest='gold_file', default='', help='The path to the file with the gold annotated instances')
    parser.add_option('--predictions_file', metavar='<PATH>',  action='store', type='string', dest='predictions_file', default='', help='The path to file with the predictions')
    parser.add_option('--output_file', metavar='<PATH>', action='store', type='string',dest='output_file', default='', help='path to the output file')
    parser.add_option('--verbose', help='Verbose output mode',  action='store_true')
    
    

    
    (options, args) = parser.parse_args(sys.argv) 
    
    if (options.gold_file==''):
        print("Error: input path to the file with gold annotations is missing!")
        print(parser.print_help())
        sys.exit(1)


    if (options.predictions_file==''):
        print("Error: input path to the predictions file is missing!")
        print(parser.print_help())
        sys.exit(1)


    if (options.output_file==''):
        print("Error: path to the output file is missing!")
        print(parser.print_help())
        sys.exit(1)


    
    evaluator=TSAR2022_SharedTask_Evaluator(options.output_file,options.verbose)
    evaluator.read_files(options.gold_file,options.predictions_file)

    
    Accuracy_at_1_at_top_gold_1=evaluator.computeAccuracy_at_N_at_top_gold_1(1)
    Accuracy_at_2_at_top_gold_1=evaluator.computeAccuracy_at_N_at_top_gold_1(2)
    Accuracy_at_3_at_top_gold_1=evaluator.computeAccuracy_at_N_at_top_gold_1(3)
    
    
    MacroAverage_Precision_at_1, MacroAverage_Recall_at_1, MacroAverage_F1_at_1, MicroAverage_Precision_at_1, MicroAverage_Recall_at_1, MicroAverage_F1_at_1, Potential_at_1=evaluator.computePrecisionMetrics_at_K(1)
    MacroAverage_Precision_at_3, MacroAverage_Recall_at_3, MacroAverage_F1_at_3, MicroAverage_Precision_at_3, MicroAverage_Recall_at_3, MicroAverage_F1_at_3, Potential_at_3=evaluator.computePrecisionMetrics_at_K(3)
    MacroAverage_Precision_at_5, MacroAverage_Recall_at_5, MacroAverage_F1_at_5, MicroAverage_Precision_at_5, MicroAverage_Recall_at_5, MicroAverage_F1_at_5, Potential_at_5=evaluator.computePrecisionMetrics_at_K(5)
    MacroAverage_Precision_at_10, MacroAverage_Recall_at_10, MacroAverage_F1_at_10, MicroAverage_Precision_at_10, MicroAverage_Recall_at_10, MicroAverage_F1_at_10, Potential_at_10=evaluator.computePrecisionMetrics_at_K(10)

    MAP_at_3=evaluator.computeMAP_at_K(3)
    MAP_at_5=evaluator.computeMAP_at_K(5)
    MAP_at_10=evaluator.computeMAP_at_K(10)
        
    
    
    factor=10000  #floor 4 decimal numbers
    
    Accuracy_at_1_at_top_gold_1_floored=math.floor(Accuracy_at_1_at_top_gold_1 * factor) / factor
    Accuracy_at_2_at_top_gold_1_floored=math.floor(Accuracy_at_2_at_top_gold_1 * factor) / factor
    Accuracy_at_3_at_top_gold_1_floored=math.floor(Accuracy_at_3_at_top_gold_1 * factor) / factor
    
    Potential_at_1_floored=math.floor(Potential_at_1 * factor) / factor
    Potential_at_3_floored=math.floor(Potential_at_3 * factor) / factor
    Potential_at_5_floored=math.floor(Potential_at_5 * factor) / factor
    Potential_at_10_floored=math.floor(Potential_at_10 * factor) / factor
    
    MAP_at_3_floored=math.floor(MAP_at_3 * factor) / factor
    MAP_at_5_floored=math.floor(MAP_at_5 * factor) / factor
    MAP_at_10_floored=math.floor(MAP_at_10 * factor) / factor
    
    
    
    evaluator.print_output_results(Potential_at_1_floored,
                                   Potential_at_3_floored,
                                   Potential_at_5_floored,
                                   Potential_at_10_floored,
                                   MAP_at_3_floored,
                                   MAP_at_5_floored,
                                   MAP_at_10_floored,
                                   Accuracy_at_1_at_top_gold_1_floored,
                                   Accuracy_at_2_at_top_gold_1_floored,
                                   Accuracy_at_3_at_top_gold_1_floored)
    
    
    
    evaluator.write_output_results(Potential_at_1_floored,
                                   Potential_at_3_floored,
                                   Potential_at_5_floored,
                                   Potential_at_10_floored,
                                   MAP_at_3_floored,
                                   MAP_at_5_floored,
                                   MAP_at_10_floored,
                                   Accuracy_at_1_at_top_gold_1_floored,
                                   Accuracy_at_2_at_top_gold_1_floored,
                                   Accuracy_at_3_at_top_gold_1_floored)




    
    
if __name__ == '__main__':
    main()

