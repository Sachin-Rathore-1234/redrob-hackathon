from pipelines.online.rank_candidates import main, parse_args


if __name__ == "__main__":
    args = parse_args()
    main(
        candidates_path=args.candidates,
        job_description_path=args.job_description,
        output_path=args.out,
        top_k=args.top_k,
    )

