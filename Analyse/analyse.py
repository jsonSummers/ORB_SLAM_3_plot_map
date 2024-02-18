import pandas as pd
import sys


def import_files(input_files):
    # Create an empty DataFrame to store concatenated data
    combined_data = pd.DataFrame()

    for input_file in input_files:
        # Extract experiment name and run number from the file path
        _, _, experiment, run, _ = input_file.split("/")
        run = int(run)

        # Read the CSV file into a DataFrame with specified data types, skipping the first row
        columns = ['point_id', 'frame', 'x', 'y', 'z', 'ClusterLabel']
        dtypes = {'point_id': int, 'frame': int, 'x': float, 'y': float, 'z': float, 'ClusterLabel': int}
        df = pd.read_csv(input_file, names=columns, dtype=dtypes, skiprows=1)

        # Add experiment and run columns to the DataFrame
        df['experiment'] = experiment
        df['run'] = run

        # Concatenate the current DataFrame with the combined data
        combined_data = pd.concat([combined_data, df], axis=0, ignore_index=True)

    return combined_data

def datamine(df):
    # number of unique points that aren't noise
    unique_non_noise_points = df[df['ClusterLabel'] != -1]['point_id'].nunique()

    # number of noise points
    noise_points = df[df['ClusterLabel'] == -1]['point_id'].nunique()

    # number of repeated observations (same point_id) that aren't noise
    repeated_non_noise_observations = df[df['ClusterLabel'] != -1]['point_id'].duplicated().sum()
    return unique_non_noise_points, noise_points, repeated_non_noise_observations

def mine_loop(df):
    # Create an empty dataframe to store results
    results_df = pd.DataFrame(
        columns=['experiment', 'run', 'unique_non_noise_points', 'noise_points', 'repeated_non_noise_observations'])

    # Iterate over unique combinations of 'experiment' and 'run'
    for (experiment, run), group in df.groupby(['experiment', 'run']):
        unique_non_noise_points, noise_points, repeated_non_noise_observations = datamine(group)

        # Append results to the results dataframe
        results_df = results_df._append({
            'experiment': experiment,
            'run': run,
            'unique_non_noise_points': unique_non_noise_points,
            'noise_points': noise_points,
            'repeated_non_noise_observations': repeated_non_noise_observations
        }, ignore_index=True)

    # Display the results dataframe
    return(results_df)

if __name__ == "__main__":
    # Get input and output file paths from command line arguments
    input_files = sys.argv[1:-1]
    output_file = sys.argv[-1]

    # Call the function to process the files
    data = import_files(input_files)
    print(data)
    final_result = mine_loop(data)
    print(final_result)
    #final_data.to_csv(output_file, index=False)
