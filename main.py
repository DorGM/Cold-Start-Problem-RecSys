import os
from data_generation import generate
from model_training import training
from model_evaluation import evaluation
from clustering import train_kmeans, train_inputfeatureskmeans
from options import config
from fuzzy_clustering import train_fuzzy_kmeans
from evaluation_with_fuzzy import evaluation_with_fuzzy
from evaluation_allocation import evaluation_with_fuzzy_allocation
from evaluation_fuzzy_only_on_cold import evaluation_with_fuzzy_on_cold
import time
import pandas as pd
import torch
import cProfile
import pstats
from pstats import SortKey

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    try:
        pd.io.parquet.get_engine('fastparquet')
    except ImportError as e:
        print("please install fastparquet first")

    if config['use_cuda'] and not torch.cuda.is_available():
        print("please make cuda gpu available, or set use_cuda=False")
        assert torch.cuda.is_available()

    master_path= "./deezer"
    dataset_path = os.getcwd() + "/data"
    embeddings_version = config["embeddings_version"]
    model_filename = "regression_model_" + embeddings_version
    clustering_path = "clustering_" + embeddings_version
    clusters_filename = "clustering_model" + embeddings_version
    fuzzy_clustering_path = "fuzzy_clustering_" + embeddings_version
    fuzzy_clusters_filename = "fuzzy_clustering_model" + embeddings_version
    inputfeaturesclustering_path = "inputfeaturesclustering_" + embeddings_version
    inputfeaturesclusters_filename = "inputfeaturesclustering_model" + embeddings_version
    print("--- running for embeddings version " + embeddings_version + " ---")

    if not os.path.exists("{}/".format(master_path)):
        os.mkdir("{}/".format(master_path))
    if not os.path.exists(master_path + "/" + embeddings_version + "/"):
        print("--- the data has not been generated yet for the embeddings version " + embeddings_version + " : generation running ---")
        os.mkdir(master_path + "/" + embeddings_version + "/")
        # preparing dataset
        print("--- data generation ---")
        start_time_data_generation = time.time()
        generate(dataset_path, master_path, config['embeddings_version'])
        print("--- data generation done ---")
        print("--- seconds ---" + str(time.time() - start_time_data_generation))
    else:
        print("--- the data has already been generated : no need to regenerate it ---")

    # # training model.
    # print("--- training prediction model ---")
    # start_time_prediction_model = time.time()
    # training(dataset_path, master_path, embeddings_version = embeddings_version, eval = True, model_save = True, model_filename = model_filename)
    # print("--- training prediction model done ---")
    # print("--- seconds ---" + str(time.time() - start_time_prediction_model))
   

    # #evaluation of the model - full personalization strategy.
    # print("--- full personalisation evaluation ---")
    # start_time_fullperso_eval = time.time()
    # evaluation(dataset_path, master_path, eval_type = "full_perso", embeddings_version = embeddings_version, model_filename = model_filename)
    # print("--- full personalisation evaluation done ---")
    # print("--- seconds ---" + str(time.time() - start_time_fullperso_eval))

    # evaluation of the model - semi personalization strategy.
    # if not os.path.exists("{}/{}/".format(master_path, clustering_path)):
    #     os.mkdir("{}/{}/".format(master_path, clustering_path))
    # if not os.path.exists(master_path + "/" + clustering_path + "/" + clusters_filename):
    #     print("--- clustering running ---")
    #     start_time_clustering = time.time()
    #     train_kmeans(dataset_path, master_path, clustering_path, config['nb_clusters'], config['max_iter'], config['random_state'], embeddings_version = embeddings_version, clusters_filename = clusters_filename)
    #     print("--- clustering done ---")
    #     print("--- seconds ---" + str(time.time() - start_time_clustering))
    # else:
    #     print("--- no need to do the clustering again ---")
    
    # print("--- semi personalisation evaluation ---")
    # start_time_semiperso_eval = time.time()
    # evaluation(dataset_path, master_path, eval_type = "semi_perso", embeddings_version = embeddings_version, model_filename = model_filename, clustering_path=clustering_path, clusters_filename = clusters_filename, nb_clusters=config["nb_clusters"])
    # print("--- semi personalisation evaluation done ---")
    # print("--- seconds ---" + str(time.time() - start_time_semiperso_eval))
    
    # fuzzy_kmeans
    # if not os.path.exists("{}/{}/".format(master_path, fuzzy_clustering_path)):
    #     os.mkdir("{}/{}/".format(master_path, fuzzy_clustering_path))
    # if not os.path.exists(master_path + "/" + fuzzy_clustering_path + "/" + clusters_filename):
    #     print("--- fuzzy clustering running ---")
    #     start_time_fuzzy_clustering = time.time()
    #     train_fuzzy_kmeans(dataset_path, master_path, fuzzy_clustering_path, config['nb_clusters'], config['max_iter'], config['random_state'], embeddings_version = embeddings_version, clusters_filename = fuzzy_clusters_filename)
    #     print("--- fuzzy clustering done ---")
    #     print("--- seconds ---" + str(time.time() - start_time_fuzzy_clustering))
    
    # print("--- fuzzy clustering evaluation ---")
    # start_time_fuzzy_eval = time.time()
    # evaluation_with_fuzzy(dataset_path, master_path, eval_type = "semi_perso", embeddings_version = embeddings_version, model_filename = model_filename, clustering_path=fuzzy_clustering_path, clusters_filename = fuzzy_clusters_filename, nb_clusters=config["nb_clusters"])
    # print("--- fuzzy clustering evaluation done ---")
    # print("--- seconds ---" + str(time.time() - start_time_fuzzy_eval))


    # print("--- fuzzy clustering allocation evaluation ---")
    # start_time_fuzzy_eval = time.time()
    # evaluation_with_fuzzy_allocation(dataset_path, master_path, eval_type = "semi_perso", embeddings_version = embeddings_version, model_filename = model_filename, clustering_path=fuzzy_clustering_path, clusters_filename = fuzzy_clusters_filename, nb_clusters=config["nb_clusters"])
    # print("--- fuzzy clustering allocation evaluation done ---")
    # print("--- seconds ---" + str(time.time() - start_time_fuzzy_eval))
   
    print("--- fuzzy clustering on cold evaluation ---")
    start_time_fuzzy_eval = time.time()
    evaluation_with_fuzzy_on_cold(dataset_path, master_path, eval_type = "semi_perso", embeddings_version = embeddings_version, model_filename = model_filename, clustering_path=clustering_path, clusters_filename = clusters_filename, nb_clusters=config["nb_clusters"])
    print("--- fuzzy clustering on cold evaluation done ---")
    print("--- seconds ---" + str(time.time() - start_time_fuzzy_eval))
   
    # input features clustering baseline.
    # print("--- input features clustering baseline evaluation ---")
    # start_time_inputfeatures_clustering = time.time()
    # if not os.path.exists("{}/{}/".format(master_path, inputfeaturesclustering_path)):
    #     os.mkdir("{}/{}/".format(master_path, inputfeaturesclustering_path))
    # if not os.path.exists(master_path + "/" + inputfeaturesclustering_path + "/" + inputfeaturesclusters_filename):
    #     print("--- input features clustering running ---")
    #     start_time_inputfeaturesclustering = time.time()
    #     train_inputfeatureskmeans(dataset_path, master_path, inputfeaturesclustering_path, config['nb_clusters_inputfeatures'], config['max_iter'], config['random_state'], config["nb_songs"], embeddings_version = embeddings_version, clusters_filename = inputfeaturesclusters_filename)
    #     print("--- clustering done ---")
    #     print("--- seconds ---" + str(time.time() - start_time_inputfeatures_clustering))
    # else:
    #     print("--- no need to do the clustering again ---")

    # input features evaluation    
    # print("--- input features clustering baseline evaluation ---")
    # start_time_inputfeaturesbaseline_eval = time.time()
    # evaluation(dataset_path, master_path, eval_type = "inputfeatures", embeddings_version = embeddings_version, model_filename = model_filename, clustering_path = inputfeaturesclustering_path, clusters_filename = inputfeaturesclusters_filename, nb_clusters = config['nb_clusters_inputfeatures'])
    # print("--- input features clustering baseline evaluation done ---")
    # print("--- seconds ---" + str(time.time() - start_time_inputfeaturesbaseline_eval))
    
    # popularity baseline.
    # print("--- popularity baseline evaluation ---")
    # start_time_popbaseline_eval = time.time()
    # evaluation(dataset_path, master_path, eval_type = "popularity", embeddings_version = embeddings_version, model_filename = model_filename)
    # print("--- popularity baseline evaluation done ---")
    # print("--- seconds ---" + str(time.time() - start_time_popbaseline_eval))
    
    # # avg d0 stream baseline.
    # print("--- avg d0 stream baseline evaluation ---")
    # start_time_avgd0streambaseline_eval = time.time()
    # evaluation(dataset_path, master_path, eval_type = "avgd0stream", embeddings_version = embeddings_version, model_filename = model_filename)
    # print("--- avg d0 stream baseline evaluation done ---")
    # print("--- seconds ---" + str(time.time() - start_time_avgd0streambaseline_eval))


    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats(SortKey.CUMULATIVE)
    stats.print_stats(20)  # Print top 20 functions by cumulative time
    # Optionally save results to a file
    stats.dump_stats("profile_results.prof")